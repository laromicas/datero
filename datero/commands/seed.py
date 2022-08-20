import os
import json
from . import Command, SEEDS_FOLDER, config
from .doctor import check_seed

class Seed:
    name = None
    path = None
    actions = {}

    def __init__(self, **kwargs) -> None:
        self.__dict__.update(kwargs)
        self.path = os.path.join(SEEDS_FOLDER, self.name)
        if os.path.exists(os.path.join(self.path,'actions.json')):
            with open(os.path.join(self.path,'actions.json'), 'r') as file:
                self.actions = json.load(file)

    def fetch(self):
        working_path = config.get('PATHS', 'WorkingPath')
        working_path = os.path.abspath(os.path.join(os.getcwd(), working_path))
        paths = {
            'SEED_NAME': self.name,
            'WORK_FOLDER': working_path,
            'TMP_FOLDER': config.get('PATHS', 'TempPath'),
            'ROMVAULT_FOLDER': config.get('PATHS', 'RomVaultPath'),
            'DAT_FOLDER': config.get('PATHS', 'DatPath'),
        }
        paths.update(os.environ)
        result = Command.execute(os.path.join(self.path, 'fetch'), cwd=self.path, env=paths)
        return result


    def process_dats(self, filter=None):
        # path = f'tmp/redump/dats/{folder}'
        dat_path = os.path.join(config.get('PATHS', 'TempPath'), self.name, 'dats')
        print(self.actions)
        # for file in os.listdir(path):
        #     if file.endswith('.dat') and (not args.dat or args.dat in file):
        #         print('Processing', file)
        #         procesor = Processor(repo='redump', file=f'{path}/{file}', actions=actions['actions'])
        #         procesor.process()
        # os.system(f'cd {Settings.DAT_ROOT} && find . -type d -empty -print -delete')
        pass