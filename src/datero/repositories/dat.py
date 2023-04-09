"""
Dat classes to parse different types of dat files.
"""
# from abc import abstractmethod
import os
from pathlib import Path
import shlex
import xmltodict

from datero.database.models.datfile import System


class DatFile:
    """ Base class for dat files. """
    name: str = None
    file: str = None
    full_name: str = None
    seed: str = None

    # calculated values
    modifier: str = None
    system_type: str = None
    company: str = None
    system: str = None
    preffix: str = None
    suffix: str = None
    suffixes = []
    date = None
    path: str = None
    version: str = None

    def __init__(self, **kwargs) -> None:
        self.__dict__.update(kwargs)
        if not self.name and not self.file:
            raise ValueError("No file specified")
        if not self.name:
            self.load()

    # @abstractmethod
    def load(self) -> None:
        """ Abstract ** Load the dat file. """

    # @abstractmethod
    def initial_parse(self) -> None:
        """ Parse the dat file. """

    # @abstractmethod
    def get_date(self) -> str:
        """ Get the date from the dat file. """

    def close(self) -> None:
        """ Close the dat file if needed. """

    def get_modifier(self) -> str:
        """ Get the modifier ej. 'Source Code', 'etc' """
        return getattr(self, 'modifier', None)

    def get_company(self) -> str:
        """ Get the company name. """
        return getattr(self, 'company', None)

    def get_system(self) -> str:
        """ Get the system name. """
        return getattr(self, 'system', None)

    def get_system_type(self) -> str:
        """ Get the system type. """
        return getattr(self, 'system_type', None)

    def get_preffix(self) -> str:
        """ Get the preffix for the path. """
        return getattr(self, 'preffix', None)

    def get_suffix(self) -> str:
        """ Get the suffix for the path. """
        return getattr(self, 'suffix', None)

    def get_path(self) -> str:
        """ Get the path for the dat file. """
        self.path = os.path.join(*[x for x in [self.get_preffix(), self.get_company(), self.get_system(), self.get_suffix()] if x])
        return self.path

    def dict(self) -> dict:
        """ Return a dictionary with the dat file information. """
        self.initial_parse()
        return {
            "name": self.name,
            "file": self.file,
            "full_name": self.full_name,
            "date": self.get_date(),
            "modifier": self.get_modifier(),
            "company": self.get_company(),
            "system": self.get_system(),
            "system_type": self.get_system_type(),
            "path": self.get_path(),
        }


class XMLDatFile(DatFile):
    """ XML dat file. """
    shas = None
    game_key = 'game'
    header = None

    def load(self) -> None:
        """ Load the data from a XML file. """
        with open(self.file, encoding='utf-8') as fild:
            self.data = xmltodict.parse(fild.read(), process_namespaces=True)
            self.header = self.data['datafile']['header']
            self.name = self.header['name'] if 'name' in self.header else None
            self.full_name = self.header['description'] if 'description' in self.header else None
            self.date = self.header['date'] if 'date' in self.header else None
            self.homepage = self.header['homepage'] if 'homepage' in self.header and self.header['homepage'] and 'insert' not in self.header['homepage'] else None
            self.url = self.header['url'] if 'url' in self.header and self.header['url'] and 'insert' not in self.header['url'] else None
            self.author = self.header['author'] if 'author' in self.header and self.header['author'] and 'insert' not in self.header['author'] else None
            self.email = self.header['email'] if 'email' in self.header and self.header['email'] and 'insert' not in self.header['email'] else None

    def get_rom_shas(self) -> None:
        """ Get the shas for the roms and creates an index. """
        for game in self.data['datafile'][self.game_key]:
            if not isinstance(game['rom'], list):
                self.shas.add_rom(game['rom'])
            else:
                for rom in game['rom']:
                    self.shas.add_rom(rom)

    def get_name(self) -> str:
        """ Get the name of the dat file. """
        if not self.name:
            self.load()
        return self.name

    def overrides(self) -> System:
        """ Overrides data for some systems. """
        find_system = System(company=self.get_company(), system=self.get_system())
        find_system.load()
        if getattr(find_system, 'system_type', None):
            self.system_type = find_system.system_type
            if getattr(find_system, 'override', None):
                self.__dict__.update(find_system.override)
        return find_system

    def extra_configs(self, find_system):
        """ Extra configs for some systems. """
        extra_configs = getattr(find_system, 'extra_configs', None)
        if extra_configs:
            if 'empty_suffix' in extra_configs and not self.suffix:
                self.suffix = extra_configs['empty_suffix'].get(self.seed, None)
            if 'additional_suffix' in extra_configs:
                self.suffix = os.path.join(self.suffix, extra_configs['additional_suffix'].get(self.seed, None))
            if 'if_suffix' in extra_configs:
                for key, value in extra_configs['if_suffix'].items():
                    if key in self.suffixes:
                        self.__dict__.update(value)

    def get_date(self):
        """ Get the date from the dat file. """
        return self.date

class ClrMameProDatFile(DatFile):
    """ ClrMamePro dat file. """
    header = {}
    games = []

    def get_next_block(self, data):
        """ Get the next block of data. """
        parenthesis = 0
        start = 0
        end = 0
        for i, char in enumerate(data):
            if char == '(':
                if parenthesis == 0:
                    start = i + 1
                parenthesis += 1
            if char == ')':
                parenthesis -= 1
            if parenthesis == 0 and start >= 1:
                end = i
                break
        return data[start:end], data[end + 1:] if end < len(data) else None

    def read_block(self, data) -> dict:
        """ Read a block of data from a ClrMame dat and parses it. """
        dictionary = {}
        for line in iter(data.splitlines()):
            line = line.strip()
            if line:
                if line.startswith('rom'):
                    line = line[6:-2]
                    rom = {'@name': None, '@crc': None, '@md5': None, '@sha1': None}
                    try:
                        data = shlex.split(line)
                    except ValueError:
                        data = line.split(' ')
                    for i in range(0, len(data), 2):
                        rom[f'@{data[i]}'] = data[i+1]
                    dictionary['rom'] = [] if 'rom' not in dictionary else dictionary['rom']
                    dictionary['rom'].append(rom)
                else:
                    try:
                        key, value = shlex.split(line)
                    except ValueError as exc:
                        raise ValueError(f'Error parsing line: {line} from: {self.file}') from exc
                    dictionary[key] = value

        return dictionary

    def load(self) -> None:
        """ Load the data from a ClrMamePro file. """
        self.games = []
        with open(self.file, encoding='utf-8', errors='ignore') as file:
            data = file.read()

            block, next_block = self.get_next_block(data)
            self.header = self.read_block(block)

            while next_block:
                block, next_block = self.get_next_block(next_block)
                self.games.append(self.read_block(block))

        self.data = {
            'datafile': {
                'header':  self.header,
                'game': self.games
            }
        }
        self.name = self.header['name']
        self.full_name = self.header['description']

    def get_rom_shas(self) -> None:
        """ TODO Method """


class ZipMultiDatFile(DatFile):
    """ Base class for dat files. """
    def get_header(self) -> dict:
        """ Get the header from the dat file. """
        return { 'name': os.path.basename(self.file), 'description': self.file }

    def load(self) -> None:
        """ Load the data from a ClrMamePro file. """
        self.games = []
        self.header = self.get_header()

        self.data = {
            'datafile': {
                'header':  self.header,
                'game': self.games
            }
        }
        self.name = self.header['name']
        self.full_name = self.header['description']

class DirMultiDatFile(DatFile):
    """ Base class for dat files. """
    def get_header(self) -> dict:
        """ Get the header from the dat file. """
        return { 'name': self.name, 'description': self.file }

    def load(self) -> None:
        """ Load the data from a ClrMamePro file. """
        self.games = []
        for file in os.listdir(self.file):
            ext = Path(file).suffix
            if ext in ['.xml', '.dat']:
                self.games.append({ 'rom': { '@name': file } })

        self.name = os.path.basename(self.file)

        self.header = self.get_header()

        self.data = {
            'datafile': {
                'header':  self.header,
                'game': self.games
            }
        }
        self.name = self.header['name']
        self.full_name = self.header['description']
