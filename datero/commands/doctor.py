import os
import re
import pkg_resources
from . import SEEDS_FOLDER, Bcolors

ignore_packages = ['pyOpenSSL', 'PySocks']


def check_seed(seed):
    if not os.path.isdir(os.path.join(SEEDS_FOLDER, seed)):
        return False
    return seed

def check_version(detected, required, expression):
    detected = pkg_resources.parse_version(detected)
    required = pkg_resources.parse_version(required)
    if expression == '>':
        return detected > required
    elif expression == '<':
        return detected < required
    elif expression == '>=':
        return detected >= required
    elif expression == '<=':
        return detected <= required
    elif expression == '==':
        return detected == required
    else:
        return detected == required

def check_installed_packages(seed, installed_pkgs):
    if os.path.isfile(os.path.join(SEEDS_FOLDER, seed, 'requirements.txt')):
        with open(os.path.join(SEEDS_FOLDER, seed, 'requirements.txt'), 'r') as req:
            all_installed = True
            for line in req:
                line = line.strip()
                if line.startswith('#') or line == '':
                    continue
                line0 = re.split('[>=<]', line)
                line0 = [x for x in line0 if x]
                if line0[0] in ignore_packages:
                    continue
                if line0[0] not in installed_pkgs:
                    print(f'{Bcolors.FAIL}  - {line}{Bcolors.ENDC} not installed')
                    all_installed = False
                    continue
                if len(line0) > 1:
                    expression = ''.join(re.findall('[>=<]', line))
                    # line0[1] = expression
                    if not check_version(detected=installed_pkgs[line0[0]], required=line0[1], expression=expression):
                        print(f'{Bcolors.FAIL}  - {line}{Bcolors.ENDC} differs from installed version (detected {installed_pkgs[line0[0]]})')
                        all_installed = False
            if all_installed:
                print(f'{Bcolors.OKGREEN}  - All requirements installed{Bcolors.ENDC}')
    else:
        print(f'{Bcolors.OKGREEN}  - All requirements installed{Bcolors.ENDC}')


def check_main_executables(seed):
    min_files = {
        '__init__.py': 'Namespace initialization file',
        'fetch': 'Fetch script',
        'Process': 'Process script'
        }
    for file, desc in min_files.items():
        if not os.path.isfile(os.path.join(SEEDS_FOLDER, seed, file)):
            print(f'{Bcolors.FAIL}  - {Bcolors.BOLD}{file}{Bcolors.ENDC} not found ({desc})')

def check_seed(seed):
    if not os.path.isdir(os.path.join(SEEDS_FOLDER, seed)):
        return False

    installed_pkgs = {pkg.key: pkg.version for pkg in pkg_resources.working_set}
    print(f'* {Bcolors.OKCYAN}{seed}{Bcolors.ENDC}')
    check_installed_packages(seed, installed_pkgs)
    check_main_executables(seed)