import os
import re
import subprocess
import sys
from shutil import which
import pkg_resources
from . import SEEDS_FOLDER, Bcolors

ignore_packages = ['pyOpenSSL', 'PySocks']


def check_seed(seed):
    return os.path.isdir(os.path.join(SEEDS_FOLDER, seed))

def check_version(detected, required, expression):
    detected = pkg_resources.parse_version(detected)
    required = pkg_resources.parse_version(required)
    match expression:
        case '>':
            return detected > required
        case '<':
            return detected < required
        case '>=':
            return detected >= required
        case '<=':
            return detected <= required
        case '==':
            return detected == required
        case _:
            return detected == required

def required_packages(seed, installed_pkgs):
    fixable = []
    not_fixable = []
    if os.path.isfile(os.path.join(SEEDS_FOLDER, seed, 'requirements.txt')):
        with open(os.path.join(SEEDS_FOLDER, seed, 'requirements.txt'), 'r') as req:
            for line in req:
                line = line.strip()
                if line.startswith('#') or line == '':
                    continue
                line0 = re.split('[>=<]', line)
                line0 = [x for x in line0 if x]
                if line0[0] in ignore_packages:
                    continue
                if line0[0] not in installed_pkgs:
                    fixable.append(line)
                    continue
                if len(line0) > 1:
                    expression = ''.join(re.findall('[>=<]', line))
                    # line0[1] = expression
                    if not check_version(detected=installed_pkgs[line0[0]], required=line0[1], expression=expression):
                        not_fixable.append((line, installed_pkgs[line0[0]]))
    return fixable, not_fixable

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def check_main_executables():
    req_executables = {
        'wget': 'wget',
        'unzip': 'unzip',
        '7z': 'p7zip',
        'geckodriver': 'geckodriver',
    }
    for exe, pkg in req_executables.items():
        if which(exe) is None and which(exe + '.exe') is None:
            print(f'{Bcolors.FAIL}  - {Bcolors.BOLD}{exe}{Bcolors.ENDC} not found (install {pkg})')


def check_needed_files(seed):
    req_files = {
        '__init__.py': 'Namespace initialization file',
        'fetch': 'Fetch script',
        'actions.json': 'json with actions to execute to process the data',
        'rules.json': 'json with rules to detect the datafile seed',
        }
    for file, desc in req_files.items():
        if not os.path.isfile(os.path.join(SEEDS_FOLDER, seed, file)):
            print(f'{Bcolors.FAIL}  - {Bcolors.BOLD}{file}{Bcolors.ENDC} not found ({desc})')


def check_dependencies(seed, repair=False):
    installed_pkgs = {pkg.key: pkg.version for pkg in pkg_resources.working_set}
    print(f'* {Bcolors.OKCYAN}{seed}{Bcolors.ENDC}')
    # check_installed_packages(seed, installed_pkgs)
    fixable, not_fixable = required_packages(seed, installed_pkgs)
    if not_fixable:
        print(f'{Bcolors.FAIL}  - Not fixable requirements:{Bcolors.ENDC}')
        for line in not_fixable:
            print(f'    - {line[0]} (detected {line[1]})')
    if fixable:
        print(f'{Bcolors.WARNING}  - Requirements not found:{Bcolors.ENDC}')
        for line in fixable:
            print(f'    - {line}')
        if repair:
            print(f'{Bcolors.OKGREEN}  - Installing requirements:{Bcolors.ENDC}')
            for line in fixable:
                print(f'    - {line}')
                install(line)
    if not fixable and not not_fixable:
        print(f'{Bcolors.OKGREEN}  - All requirements installed{Bcolors.ENDC}')
    check_needed_files(seed)

