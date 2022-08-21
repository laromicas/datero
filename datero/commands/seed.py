import os
import json
from . import Command, SEEDS_FOLDER, config, ROOT_FOLDER
from actions.processor import Processor


class Seed:
    name = None
    path = None
    actions = {}
    working_path = os.path.abspath(os.path.join(os.getcwd(), config.get('PATHS', 'WorkingPath')))

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
        for path, actions in self.actions.items():
            new_path = path.format(dat_path=dat_path)
            for file in os.listdir(new_path):
                if file.endswith('.dat') and (not filter or filter in file):
                    print('Processing', file)
                    procesor = Processor(seed=self.name, file=f'{new_path}/{file}', actions=actions)
                    procesor.process()
