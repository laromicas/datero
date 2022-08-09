import re
import os
from tinydb import Query
from lib.dat import XMLDatFile
from lib.database.models import Dat
from lib import Settings
from lib.database.models.datfile import System


class NoIntroDat(XMLDatFile):


    date_in_name = False
    repo: str = 'nointro'
    name: str = None
    full_name: str = None
    file: str = None
    modifier: str = None
    company: str = None
    system: str = None
    system_type: str = None
    preffix: str = None
    suffix: str = None
    path: str = None

    def initial_parse(self) -> list:
        name = self.name

        suffixes = re.findall('\(.*?\)', self.full_name)
        name = name.replace(' '.join(suffixes), '').strip()
        name_array = name.split(' - ')

        if suffixes:
            suffixes = [x[1:-1] for x in suffixes]

        if name_array[0] == 'Non-Redump':
            suffixes.append('ExtraDiscs')
            name_array.pop(0)
        elif name_array[0] == 'Unofficial':
            name_array.pop(0)
            if 'Magazine Scans' not in name:
                suffixes.append('UnofficialDiscs')
        # name_array = list(dict.fromkeys(name_array))

        preffixes = []
        if name_array[0] == 'Source Code':
            preffixes.append(name_array.pop(0))
            self.modifier = 'Source Code'

        if len(name_array) > 2:
            name_array[1] = f'{name_array[1]} {Settings.UNION_CHARACTER} {name_array.pop()}'

        if len(name_array) == 1:
            name_array.insert(0, None)

        company, system = name_array
        self.company = company
        self.system = system
        if suffixes:
            self.suffix = os.path.join(*suffixes)

        self.suffixes = suffixes
        find_system = self.overrides()
        self.extra_configs(find_system)

        self.preffix = Settings.Preffixes.get(self.modifier or self.system_type, '')

        return [self.preffix, self.company, self.system, self.suffix, self.get_date()]


    def get_date(self) -> str:
        if self.date:
            return self.date
        elif self.file:
            result = re.findall('\(.*?\)', self.file)
            self.date = result[len(result)-1][1:-1]
        return self.date


    def dict(self) -> dict:
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
            "path": self.get_path()
        }