import configparser
import json
import logging
import os
from pathlib import Path
from pydoc import locate
import re
import sys
import argparse
import pkg_resources
from tabulate import tabulate
from datero.configuration.logger import enable_logging, set_verbosity
from datero.database.models.datfile import Dat

from datero.helpers import Bcolors
from datero.helpers.executor import Command
from datero.configuration import config

from datero.commands.list import installed_seeds, seed_description
from datero.commands.doctor import check_seed, check_installed_packages, check_main_executables
from datero.commands.seed_manager import seed_available, get_seed_repository, seed_install, seed_remove
from datero.commands.seed import Seed
from datero.seeds.rules import Rules
from datero.seeds.unknown_seed import detect_seed

#---------Boilerplate to check python version ----------
if sys.version_info[0] < 3:
    print("This is a Python 3 script. Please run it with Python 3.")
    exit(1)


def parse_args():
    parser = argparse.ArgumentParser(description='Update dats from different sources.')
    subparser = parser.add_subparsers(help='sub-command help')

    parser.add_argument('-v', '--version', action='store_true', help='show version')

    parser_save = subparser.add_parser('config', help='Show configuration')
    parser_save.add_argument('-s', '--save', action='store_true', help='Save configuration to .daterorc')
    parser_save.set_defaults(func=command_config)
    parser_save.add_argument('-ru', '--rules-update', action='store_true', help='Update system rules from GoogleSheets Url')

    group_save = parser_save.add_mutually_exclusive_group()
    group_save.add_argument('--set', nargs=2, metavar=('configuration', 'value'), help='Set Configuration Option separated by point with new value e.g. <GENERAL.Overwrite> <false>')
    group_save.add_argument('--get', metavar=('configuration'), help='Get value of Configuration Option.')
    parser_save.add_argument('-g','--global', action='store_true', help='When set, saves to global config, else to `.daterorc`')

    parser_list = subparser.add_parser('list', help='List installed seeds')
    parser_list.set_defaults(func=command_list)

    parser_doctor = subparser.add_parser('doctor', help='Doctor installed seeds')
    parser_doctor.add_argument('command', nargs='?', help='Seed to doctor')
    parser_doctor.set_defaults(func=command_doctor)

    parser_dat = subparser.add_parser('dat', help='Make changes in dat config')
    parser_dat.add_argument('command', nargs='?', help='Command to execute')
    group_dat= parser_dat.add_mutually_exclusive_group(required=True)

    group_dat.add_argument('-d', '--dat-name', help='Select dat to update/check, must be in format "seed:name"')
    group_dat.add_argument('-s', '--search', help='Select dats based on filter, they are "<field><operator><value>;...", valid operators are: =, !=, and ~=')
    parser_dat.add_argument('-ss', '--set-status', help='Select all dats', choices=['enabled', 'disabled'])
    parser_dat.add_argument('-on', '--only-names', action='store_true', help='Only show names')

    # parser_dat.add_argument('-t', '--table', default='dats', help='Select table', choices=['dats', 'systems'])

    parser_dat.set_defaults(func=command_dat)

    """ Seed admin commands """
    parser_seed = subparser.add_parser('seed', help='Seed scripts')
    subparser_seed = parser_seed.add_subparsers(help='sub-command help')

    parser_available = subparser_seed.add_parser('available', help='List available seeds')
    parser_available.set_defaults(func=command_seed_available)

    parser_install = subparser_seed.add_parser('install', help='Install seed')
    parser_install.add_argument('seed', help='Seed to install')
    parser_install.set_defaults(func=command_seed_install)
    parser_install.add_argument('-r', '--repository', help='Use repository instead of default')
    parser_install.add_argument('-b', '--branch', help='Use branch name instead of master')
    parser_install.add_argument('-d', '--developer', action='store_true', help='Install developer version (with git)')
    parser_install.add_argument('-id', '--install-dependencies', action='store_true', help='Install all required dependencies')

    parser_remove = subparser_seed.add_parser('remove', help='Remove seed')
    parser_remove.add_argument('seed', help='Seed to remove')
    parser_remove.set_defaults(func=command_seed_remove)

    parser_import = subparser.add_parser('import', help='Import dats from existing romvault')
    # parser_import.add_argument('path', help='DatRoot path')
    parser_import.set_defaults(func=command_dat_import)


    """ Seed commands """
    commands = []
    for seed in list(installed_seeds()) + [('all', 'All seeds')]:
        parser_command = subparser.add_parser(seed[0], help=f'Update seed {seed[0]}')
        parser_command.set_defaults(func=command_seed, seed=seed[0])
        parser_command.add_argument('-f', '--fetch', action='store_true', help='Fetch seed')
        parser_command.add_argument('-p', '--process', action='store_true', help='Process dats from seed')
        parser_command.add_argument('-fd', '--filter', help='Filter dats to process')
        commands.append(parser_command)

    """ Common arguments """
    subparsers = [subparser, subparser_seed]
    for subpars in subparsers:
        for subpar in subpars.choices.values():
            subpar.add_argument('-v', '--verbose', action='store_true', help='verbose output')
            subpar.add_argument('-q', '--quiet', action='store_true', help='quiet output')
            subpar.add_argument('-nc', '--no-color', action='store_true', help='disable color output')
            subpar.add_argument('-l', '--logging', action='store_true', help='enable logging')

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()
    if getattr(args, 'version', False):
        from . import __version__
        print(__version__)
        sys.exit()

    if getattr(args, 'no_color', False) or os.name == 'nt':
            Bcolors.no_color()
    if getattr(args, 'quiet', False):
        set_verbosity(logging.WARNING)
        config['COMMAND']['Quiet'] = 'true'
    if getattr(args, 'verbose', False):
        set_verbosity(logging.DEBUG)
        config['COMMAND']['Verbose'] = 'true'
    if getattr(args, 'logging', False):
        enable_logging()
    return args

def command_dat(args):
    """Make changes in dat config"""
    from datero.database import DB
    from tinydb import Query
    query = Query()
    table = DB.table('dats')
    output = []
    if args.dat_name:
        splitted = args.dat_name.split(':')
        if len(splitted) != 2:
            print(f'{Bcolors.WARNING}Invalid dat name, must be in format "seed:name"{Bcolors.ENDC}')
            print(f'Showing results for filter: {Bcolors.OKCYAN}name~={args.dat_name}{Bcolors.ENDC}')
            print('--------------------------------------------------------------')
            name = args.dat_name
            result = table.search(query.name.matches(r'^.*' + name + r'.*', flags=re.IGNORECASE))
            if getattr(args, 'only_names', False):
                for dat in result:
                    print(f"{dat['seed']}:{dat['name']}")
                sys.exit()
            for dat in result:
                output.append({
                    'seed': dat['seed'],
                    'name': dat['name'],
                    'status': dat['status'] if 'status' in dat else 'enabled',
                })
            print(tabulate(output, headers='keys', tablefmt='psql'))
            sys.exit(0)
        else:
            seed, name = splitted
            result = table.get((query.name == name) & (query.seed == seed))
            if not result:
                print(f'{Bcolors.FAIL}Dat not found{Bcolors.ENDC}')
                sys.exit(1)
            if args.set_status:
                table.update({'status': args.set_status}, doc_ids=[result.doc_id])
                table.storage.flush()
                print(f'{Bcolors.OKGREEN}Dat {Bcolors.OKCYAN}{seed}:{name}{Bcolors.OKGREEN} status set to {Bcolors.OKBLUE}{args.set_status}{Bcolors.ENDC}')
                sys.exit(0)
            if result:
                output.append({
                    'seed': result['seed'],
                    'name': result['name'],
                    'status': result['status'] if 'status' in result else 'enabled',
                })
            print(tabulate(output, headers='keys', tablefmt='psql'))
            sys.exit(0)

def command_dat_import(args):
    """Make changes in dat config"""
    # config_dict = {s:dict(config.items(s)) for s in config.sections()}
    dat_root_path = config['PATHS']['DatPath']
    rules = Rules().rules

    dats = { str(x):None for x in Path(dat_root_path).rglob("*.[dD][aA][tT]") }
    if config['IMPORT'].get('IgnoreRegEx'):
        ignore_regex = re.compile(config['IMPORT']['IgnoreRegEx'])
        dats = [ dat for dat in dats if not ignore_regex.match(dat) ]

    fromhere = '/mnt/d/ROMVault/DatRoot/Consoles/Nintendo/Nintendo Entertainment System/NRS/NES 2.0 (NRS) B (1.20211225.R6M5) Headered.dat'
    found = False
    for dat_name in dats:
        if dat_name == fromhere:
            found = True
        if not found:
            continue
        print(f'{dat_name} - ', end='')
        seed, class_detected = detect_seed(dat_name, rules)
        print(f'{seed} - {class_detected}')
        if class_detected:
            class_name = locate(class_detected)
            dat = class_name(file=dat_name)
            dat.load()
            database = Dat(seed=seed, new_file=dat_name, **dat.dict())
            database.save()
            database.close()


def command_seed_remove(args):
    """Remove seed"""
    if not check_seed(args.seed):
        print(f'Module Seed {Bcolors.FAIL}  - {Bcolors.BOLD}{args.seed}{Bcolors.ENDC} not found')
        exit(1)
    seed_remove(args.seed)
    print(f'Seed {Bcolors.OKGREEN}{args.seed}{Bcolors.ENDC} removed successfully')

def command_seed_install(args):
    """Install seed"""
    if check_seed(args.seed):
        print(f'Module Seed {Bcolors.WARNING}{args.seed}{Bcolors.ENDC} already installed')
        print('Reinstall? [y/n]: ', end='')
        if input().lower() != 'y':
            sys.exit(1)
    repository = get_seed_repository(args.seed) or (args.repository if getattr(args, 'repository', None) else None)
    if not repository:
        print(f'{Bcolors.FAIL}Repository for seed {args.seed} not found.{Bcolors.ENDC}')
        print('Please provide it with --repository parameter.')
        exit(1)
    seed_install(args, repository)
    print(f'Seed {Bcolors.OKGREEN}{args.seed}{Bcolors.ENDC} installed successfully')

def command_seed_available(args):
    """List available seeds"""
    status = {
        'installed': Bcolors.OKGREEN,
        'not installed': Bcolors.OKCYAN,
    }
    print('Available seeds:')
    for seed in seed_available():
        installed = 'installed' if check_seed(seed[0]) else 'not installed'
        print(f'* {status[installed]}{seed[0]}{Bcolors.ENDC} - {seed[1][0:60] if len(seed[1]) > 60 else seed[1]}...')

def command_seed(args):
    """Commands with the seed (must be installed)"""
    if args.seed == 'all':
        for seed in installed_seeds():
            args.seed = seed[0]
            command_seed(args)
        sys.exit(0)
    seed = Seed(name=args.seed)
    if getattr(args, 'fetch', False):
        print(f'Fetching seed {Bcolors.OKGREEN}{args.seed}{Bcolors.ENDC}')
        if seed.fetch():
            print(f'Errors fetching {Bcolors.FAIL}{args.seed}{Bcolors.ENDC}')
            print('Please enable logs for more information or use -v parameter')
            command_doctor(args)
    if getattr(args, 'process', False):
        print('=======================')
        print(f'{Bcolors.OKCYAN}Processing seed {Bcolors.OKGREEN}{args.seed}{Bcolors.ENDC}')
        print('=======================')
        if seed.process_dats(filter=getattr(args, 'filter', None)):
            print(f'Errors processing {Bcolors.FAIL}{args.seed}{Bcolors.ENDC}')
            print('Please enable logs for more information or use -v parameter')
            command_doctor(args)

def command_config(args):
    """Config commands"""
    if args.save:
        with open('.daterorc', 'w') as file:
            config.write(file)
        print(f'Config saved to {Bcolors.OKGREEN}.daterorc{Bcolors.ENDC}')
    elif args.set:
        myconfig = args.set[0].split('.')
        if len(myconfig) != 2:
            print(f'{Bcolors.FAIL}Invalid config key, must be in <SECTION>.<Option> format. {Bcolors.ENDC}')
            sys.exit(1)
        if myconfig[1] not in config[myconfig[0]]:
            print(f'{Bcolors.FAIL}Invalid config option. {Bcolors.ENDC}')
            sys.exit(1)

        from . import ROOT_FOLDER

        newconfig = configparser.ConfigParser(comment_prefixes='/', allow_no_value=True)
        newconfig.optionxform = lambda option: option
        if getattr(args, 'global', False):
            file = os.path.join(ROOT_FOLDER, 'datero.ini')
        else:
            file = os.path.join(os.getcwd(), '.daterorc')
        newconfig.read(file)
        if not newconfig.has_section(myconfig[0]):
            newconfig.add_section(myconfig[0])
        newconfig[myconfig[0]][myconfig[1]] = args.set[1]
        with open(file, 'w') as file:
            newconfig.write(file)
        if getattr(args, 'global', False):
            print(f'{Bcolors.OKGREEN}Global config {Bcolors.OKCYAN}{myconfig[0]}.{myconfig[1]}{Bcolors.OKGREEN} set to {Bcolors.OKBLUE}{args.set[1]}{Bcolors.ENDC}')
        else:
            print(f'{Bcolors.OKGREEN}Local Config {Bcolors.OKCYAN}{myconfig[0]}.{myconfig[1]}{Bcolors.OKGREEN} set to {Bcolors.OKBLUE}{args.set[1]}{Bcolors.ENDC}')
    elif args.get:
        myconfig = args.get.split('.')
        if len(myconfig) != 2:
            print(myconfig)
            print(f'{Bcolors.FAIL}Invalid config key, must be in <SECTION>.<Option> format. {Bcolors.ENDC}')
            sys.exit(1)
        if myconfig[1] not in config[myconfig[0]]:
            print(f'{Bcolors.FAIL}Invalid config option. {Bcolors.ENDC}')
            sys.exit(1)
        print(config[myconfig[0]][myconfig[1]])
    elif args.rules_update:
        from datero.database.seeds import dat_rules
        print('Updating rules')
        try:
            dat_rules._import_()
            print('Rules updated')
        except Exception as e:
            print(f'{Bcolors.FAIL}Error updating rules{Bcolors.ENDC}')
            print(e)
            print('Please enable logs for more information or use -v parameter')
            command_doctor(args)
    else:
        config_dict = {s:dict(config.items(s)) for s in config.sections()}
        print(json.dumps(config_dict, indent=4))


def command_list(args): # pylint: disable=unused-argument
    """List installed seeds"""
    seeds = installed_seeds()
    for seed in seeds:
        print(f'* {Bcolors.OKCYAN}{seed[0]}{Bcolors.ENDC} - {seed[1][0:60] if len(seed[1]) > 60 else seed[1]}...')

def command_doctor(args):
    """Doctor installed seeds"""
    if getattr(args, 'seed', False):
        seed = check_seed(args.seed)
        if not seed:
            print(f'Module Seed {Bcolors.FAIL}  - {Bcolors.BOLD}{args.seed}{Bcolors.ENDC} not found')
            exit(1)
        seeds = [(args.seed, seed_description(args.seed))]
    else:
        seeds = installed_seeds()
    installed_pkgs = {pkg.key: pkg.version for pkg in pkg_resources.working_set}
    for seed in seeds:
        print(f'* {Bcolors.OKCYAN}{seed[0]}{Bcolors.ENDC}')
        check_installed_packages(seed[0], installed_pkgs)
        check_main_executables(seed[0])


def main():
    """Main function"""
    args = parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
