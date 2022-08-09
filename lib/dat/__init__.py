import os
import shlex
import xmltodict

from lib.database.models.datfile import System

class DatFile:

    name = None
    file = None

    def __init__(self, **kwargs) -> None:
        self.__dict__.update(kwargs)
        if not self.name and not self.file:
            raise ValueError("No file specified")

    def load(self) -> None:
        pass

    def close(self) -> None:
        pass

    def get_modifier(self):
        return getattr(self, 'modifier', None)

    def get_company(self):
        return getattr(self, 'company', None)

    def get_system(self):
        return getattr(self, 'system', None)

    def get_system_type(self):
        return getattr(self, 'system_type', None)

    def get_preffix(self):
        return getattr(self, 'preffix', None)

    def get_suffix(self):
        return getattr(self, 'suffix', None)

    def get_path(self):
        self.path = os.path.join(*[x for x in [self.get_preffix(), self.get_company(), self.get_system(), self.get_suffix()] if x])
        return self.path


class XMLDatFile(DatFile):

    shas = None
    game_key = 'game'
    file = None
    name = None
    full_name = None
    repo = 'redump'

    def load(self) -> None:
        with open(self.file) as fd:
            self.data = xmltodict.parse(fd.read(), process_namespaces=True)
            header = self.data['datafile']['header']
            self.name = header['name'] if 'name' in header else None
            self.full_name = header['description'] if 'description' in header else None
            self.date = header['date'] if 'date' in header else None

    def get_rom_shas(self) -> None:
        for game in self.data['datafile'][self.game_key]:
            if not isinstance(game['rom'], list):
                self.shas.add_rom(game['rom'])
            else:
                for rom in game['rom']:
                    self.shas.add_rom(rom)

    def get_name(self) -> str:
        if not self.name:
            self.load()
        return self.name

    def overrides(self) -> System:
        find_system = System(company=self.get_company(), system=self.get_system())
        find_system.load()
        if getattr(find_system, 'system_type', None):
            self.system_type = find_system.system_type
            if getattr(find_system, 'override', None):
                self.__dict__.update(find_system.override)
        return find_system

    def extra_configs(self, find_system):
        extra_configs = getattr(find_system, 'extra_configs', None)
        if extra_configs:
            if 'empty_suffix' in extra_configs:
                if not self.suffix:
                    self.suffix = extra_configs['empty_suffix'].get(self.repo, None)
            if 'additional_suffix' in extra_configs:
                self.suffix = os.path.join(self.suffix, extra_configs['additional_suffix'].get(self.repo, None))
            if 'if_suffix' in extra_configs:
                for key, value in extra_configs['if_suffix'].items():
                    if key in self.suffixes:
                        self.__dict__.update(value)


class ClrMameProDatFile(DatFile):

    repo = 'redump'

    def __init__(self, **kwargs) -> None:
        self.__dict__.update(kwargs)
        if not self.name and not self.file:
            raise ValueError("No file specified")
        if not self.name:
            self.load()
        super().__init__(**kwargs)

    def load(self) -> None:
        header = {}
        games = []
        with open(self.file) as fd:
            while True:
                line = fd.readline()
                if not line:
                    break
                line = line.strip()
                if line.startswith('clrmamepro'):
                    while not line.startswith(')'):
                        line = fd.readline()
                        line = line.strip()
                        if not line or line.startswith(')'):
                            break
                        key, value = shlex.split(line)
                        header[key] = value
                if line.startswith('game'):
                    game = {'rom': []}
                    while not line.startswith(')'):
                        line = fd.readline()
                        line = line.strip()
                        if not line or line.startswith(')'):
                            break
                        if line.startswith('rom'):
                            line = line[6:-2]
                            rom = {'@name': None, '@crc': None, '@md5': None, '@sha1': None}
                            data = shlex.split(line)
                            for i in range(0, len(data), 2):
                                rom[f'@{data[i]}'] = data[i+1]
                            game['rom'].append(rom)
                        else:
                            key, value = shlex.split(line)
                            game[key] = value
                    games.append(game)
        self.data = {
            'datafile': {
                'header':  header,
                'game': games
            }
        }
        self.name = header['name']
        self.full_name = header['description']

    def get_rom_shas(self) -> None:
        pass

    def get_name(self) -> str:
        pass

    def dict(self) -> dict:
        return {'name': self.name, 'full_name': self.full_name}
