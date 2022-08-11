"""
    No-Intro Dat class.
"""
import re
import os
from lib.dat import ClrMameProDatFile, XMLDatFile
from lib import Settings


class NoIntroDat(XMLDatFile):
    """ NoIntro Dat class. """
    repo: str = 'nointro'

    def initial_parse(self) -> list:
        """ Parse the dat file. """
        # pylint: disable=R0801
        name = self.name

        suffixes = re.findall(r'\(.*?\)', self.full_name)
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
        """ Get the date from the dat file. """
        if self.date:
            return self.date
        if self.file:
            result = re.findall(r'\(.*?\)', self.file)
            self.date = result[len(result)-1][1:-1]
        return self.date


class NoIntroClrMameDat(ClrMameProDatFile):
    """ NoIntro Dat class. """
    repo: str = 'nointro'

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
        self.date = self.version
        return self.version
