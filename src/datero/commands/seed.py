import os
import json
import sys
from tabnanny import verbose
import time
from time import sleep
# mytime0 = time.time()
from . import Bcolors, Command, SEEDS_FOLDER, config, ROOT_FOLDER
# mytime1 = time.time()
# print(f"--- {mytime1 - mytime0} seconds ---")
from datero.actions.processor import Processor
# mytime2 = time.time()
# print(f"--- {mytime2 - mytime1} seconds ---")

class Seed:
    name = None
    path = None
    actions = {}
    working_path = os.path.abspath(os.path.join(os.getcwd(), config.get('PATHS', 'WorkingPath')))
    status_to_show = ['Updated', 'Added', 'Error']

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
                if file.endswith('.dat') and (not filter or filter in file):
                    if not Command.quiet:
                        self.delete_line(line)
                        line = f'Processing {Bcolors.OKCYAN}{file}{Bcolors.ENDC}'
                        print(line, end=' ', flush=True)
                    procesor = Processor(seed=self.name, file=f'{new_path}/{file}', actions=actions)
                    output = [x for x in procesor.process() if (x in self.status_to_show or Command.verbose)]
                    if not Command.quiet:
                        # [print('\b \b', end='') for x in range(0, len(line))]
                        self.delete_line(line)
                        line = f'Processed {Bcolors.OKCYAN}{file}{Bcolors.ENDC}'
                        print(line, end=' ', flush=True)

                    if output and not Command.quiet:
                        line += str(output)+' '
                        print(output, end=' ', flush=True)
                    if output or Command.verbose:
                        line = ''
                        print(line)
        self.delete_line(line)
        print(f'{Bcolors.OKBLUE}Finished processing {Bcolors.OKGREEN}{self.name}{Bcolors.ENDC}')

    def delete_line(self, line):
        # print(f'\r{line}', end='')
        [print('\b \b', end='') for x in range(0, len(line))]
        print(' ' * (len(line)), end='')
        print(f'\r', end='')