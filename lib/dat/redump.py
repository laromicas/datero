import os
import re
from lib import Settings
from lib.dat import XMLDatFile, ClrMameProDatFile


class RedumpDat(XMLDatFile):

    name: str = None
    file: str = None
    modifier: str = None
    company: str = None
    system: str = None
    system_type: str = None
    date = None
    path: str = None
    preffix = None
    suffixes = []
    suffix = None

    def initial_parse(self) -> list:
        name = self.name

        suffixes = re.findall('\(.*?\)', self.full_name)
        name = name.replace(' '.join(suffixes), '').strip()
        name_array = name.split(' - ')

        if name_array[0] == 'Arcade':
            self.modifier = name_array.pop(0)

        if len(name_array) == 1:
            name_array.insert(0, None)

        if len(name_array) > 2:
            name_array = ['-'.join(name_array[0:-1]), name_array[-1:][0]]

        company, system = name_array
        self.company = company
        self.system = system
        self.suffix = None

        self.suffixes = suffixes
        find_system = self.overrides()
        self.extra_configs(find_system)

        self.preffix = Settings.Preffixes.get(self.modifier or self.system_type, '')

        return [self.preffix, self.company, self.system, self.suffix, self.get_date()]


    def get_date(self) -> str:
        if self.full_name:
            result = re.findall('\(.*?\)', self.full_name)
            self.date = result[len(result)-1][1:-1]
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
            "path": self.get_path(),
        }


class RedumpBiosDat(ClrMameProDatFile):

    name: str = None
    file: str = None
    modifier: str = None
    company: str = None
    system: str = None
    system_type: str = None
    date = None
    path: str = None
    preffix = None
    suffixes = []
    suffix = None

    def __init__(self, **kwargs) -> None:
        self.system_type = 'BIOS'
        super().__init__(**kwargs)

    def initial_parse(self) -> list:
        name = self.name

        suffixes = re.findall('\(.*?\)', self.full_name)
        name = name.replace(' '.join(suffixes), '').strip()
        name_array = name.split(' - ')

        self.modifier = name_array.pop()

        company, system = name_array
        self.company = company
        self.system = system
        self.suffix = None

        self.suffixes = suffixes

        self.preffix = Settings.Preffixes.get(self.modifier or self.system_type, '')

        return [self.preffix, self.company, self.system, self.suffix, self.get_date()]

    def get_date(self) -> str:
        if self.full_name:
            result = re.findall('\(.*?\)', self.full_name)
            self.date = result[1][1:-1]
        elif self.file:
            result = re.findall('\(.*?\)', self.file)
            self.date = result[1][1:-1]
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
            "path": self.get_path(),
        }
