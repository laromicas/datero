"""
    ReDump Dat classes to parse different types of dat files.
"""
import re
from lib import Settings
from lib.dat import XMLDatFile, ClrMameProDatFile


class RedumpDat(XMLDatFile):
    """ Redump XML Dat class. """
    repo: str = 'redump'

    def initial_parse(self) -> list:
        """ Parse the dat file. """
        # pylint: disable=R0801
        name = self.name

        suffixes = re.findall(r'\(.*?\)', self.full_name)
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
        """ Get the date from the dat file. """
        if self.full_name:
            result = re.findall(r'\(.*?\)', self.full_name)
            if result:
                self.date = result[len(result)-1][1:-1]
        elif self.file:
            result = re.findall(r'\(.*?\)', self.file)
            if result:
                self.date = result[len(result)-1][1:-1]
        return self.date


class RedumpBiosDat(ClrMameProDatFile):
    """ Redump BIOS Dat class. """
    system_type: str = 'BIOS'
    repo: str = 'redump'

    def initial_parse(self) -> list:
        """ Parse the dat file. """
        # pylint: disable=R0801
        name = self.name

        suffixes = re.findall(r'\(.*?\)', self.full_name)
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
        """ Get the date from the dat file. """
        if self.full_name:
            result = re.findall(r'\(.*?\)', self.full_name)
            if result:
                self.date = result[1][1:-1]
        elif self.file:
            result = re.findall(r'\(.*?\)', self.file)
            if result:
                self.date = result[1][1:-1]
        return self.date
