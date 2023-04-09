import logging
from operator import le
import os
import json
from pathlib import Path
import re
from . import Bcolors, Command, SEEDS_FOLDER, config, ROOT_FOLDER
from datero.actions.processor import Processor

class Seed:
    name = None
    path = None
    actions = {}
    working_path = os.path.abspath(os.path.join(os.getcwd(), config.get('PATHS', 'WorkingPath')))
    status_to_show = ['Updated', 'Created', 'Error', 'Disabled']

    def __init__(self, **kwargs) -> None:
        self.__dict__.update(kwargs)
        self.path = os.path.join(SEEDS_FOLDER, self.name)
        if os.path.exists(os.path.join(self.path,'actions.json')):
            with open(os.path.join(self.path,'actions.json'), 'r') as file:
                self.actions = json.load(file)

    def fetch(self):
        paths = {
            'SEED_NAME': self.name,
            'WORK_FOLDER': self.working_path,
            'TMP_FOLDER': config.get('PATHS', 'TempPath'),
            'ROMVAULT_FOLDER': config.get('PATHS', 'RomVaultPath'),
            'DAT_FOLDER': config.get('PATHS', 'DatPath'),
            'DATERO_HOME': ROOT_FOLDER,
        }
        paths.update(os.environ)
        result = Command.execute(os.path.join(self.path, 'fetch'), cwd=self.path, env=paths)
        return result


    def process_dats(self, filter=None):
        dat_path = os.path.join(self.working_path, config.get('PATHS', 'TempPath'), self.name, 'dats')
        line = ''
        for path, actions in self.actions.items():
            new_path = path.format(dat_path=dat_path)
            for file in os.listdir(new_path):
                if config['PROCESS'].get('DatIgnoreRegEx'):
                    ignore_regex = re.compile(config['PROCESS']['DatIgnoreRegEx'])
                    if ignore_regex.match(file):
                        continue
                ext = Path(file).suffix
                if (ext in ('.dat', '.xml')) and (not filter or filter in file):
                    if not config.getboolean('COMMAND', 'Quiet', fallback=False):
                        self.delete_line(line)
                        line = f'Processing {Bcolors.OKCYAN}{file}{Bcolors.ENDC}'
                        print(line, end=' ', flush=True)
                    procesor = Processor(seed=self.name, file=f'{new_path}/{file}', actions=actions)
                    output = [x for x in procesor.process() if (x in self.status_to_show or Command.verbose)]
                    if 'Deleted' in output and 'Ignored' in output:
                        output.append('Disabled')
                    if not config.getboolean('COMMAND', 'Quiet', fallback=False):
                        # [print('\b \b', end='') for x in range(0, len(line))]
                        self.delete_line(line)
                        line = f'Processed {Bcolors.OKCYAN}{file}{Bcolors.ENDC}'
                        print(line, end=' ', flush=True)

                    if output and not config.getboolean('COMMAND', 'Quiet', fallback=False):
                        line += str(output)+' '
                        print(output, end=' ', flush=True)
                    if output or config.getboolean('COMMAND', 'Verbose', fallback=False):
                        line = ''
                        print(line)
        self.delete_line(line)
        print(f'{Bcolors.OKBLUE}Finished processing {Bcolors.OKGREEN}{self.name}{Bcolors.ENDC}')

    def delete_line(self, line):
        # print(f'\r{line}', end='')
        [print('\b \b', end='') for x in range(0, len(line))]
        print(' ' * (len(line)), end='')
        print('\r', end='')