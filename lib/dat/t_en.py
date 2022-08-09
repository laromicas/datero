import os
import re
from lib import Settings
from lib.dat import XMLDatFile

class TranslatedEnglishDat(XMLDatFile):

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

    def initial_parse(self):
        name = self.name

        name = name.split('[T-En]')[0].strip()
        name_array = name.split(' - ')

        company, system = name_array
        self.company = company
        self.system = system
        self.suffix = 'Translated-English'
        self.overrides()

        self.preffix = Settings.Preffixes.get(self.modifier or self.system_type, '')

        return [self.preffix, self.company, self.system, self.suffix, self.get_date()]


    def get_date(self):
        if self.file:
            result = re.findall('\(.*?\)', self.file)
            self.date = result[len(result)-1][1:-1]
        return self.date

    # def get_modifier(self):
    #     return None

    # def get_company(self):
    #     def detect_company(name):
    #         company = re.findall(r'.+?(?=\ -\ )', name)
    #         return company[0] if company else name

    #     if self.company:
    #         return self.company.strip()
    #     self.company = detect_company(self.name).strip()
    #     return self.company.strip()

    # def get_system(self):
    #     def detect_system(name, company):
    #         if company:
    #             name = name.replace(company + " - ", "")
    #         name = name.split('[T-En]')[0]
    #         if 'PC Engine CD' in name:
    #             return 'PC Engine CD & TurboGrafx CD'
    #         if 'PC Engine' in name:
    #             return 'PC Engine - TurboGrafx 16'
    #         if 'PC-9801' in name:
    #             return 'PC-98'
    #         if 'PC-8801' in name:
    #             return 'PC-88'
    #         if 'PC-FX' in name:
    #             return 'PC-FX & PC-FXGA'
    #         if 'Super Famicom' in name:
    #             return 'Super Nintendo Entertainment System'
    #         if 'Famicom' in name:
    #             return 'Nintendo Entertainment System'
    #         if 'Master System' in name:
    #             return 'Master System - Mark III'
    #         if 'Mega CD' in name:
    #             return 'Mega CD & Sega CD'
    #         if 'Mega Drive' in name:
    #             return 'Mega Drive - Genesis'
    #         return name.strip()

    #     if self.system:
    #         return self.system.strip()
    #     self.system = detect_system(self.name, self.get_company())
    #     return self.system.strip()

    # def get_folder(self):
    #     self.folder['preffix'] = f'{self.get_modifier()}'
    #     # Patches for some systems Preffix
    #     if self.get_company() in ('Mobile'):
    #         self.folder['preffix'] = 'Phone'
    #     elif self.get_company() in ('ACT', 'Acorn', 'Amstrad', 'Apple', 'Commodore', 'Fujitsu', 'Fukutake Publishing',
    #                               'Hitachi', 'IBM', 'Luxor', 'Sharp', 'TeleNova', 'Texas Instruments'
    #                               ):
    #         self.folder['preffix'] = 'Computer'
    #     elif self.get_company() in ('Microsoft') and self.get_system().startswith('MSX'):
    #         self.folder['preffix'] = 'Computer'
    #     elif self.get_system() in ('PC-98', 'PC-88', 'PC-8001', 'PC-6001'):
    #         self.folder['preffix'] = 'Computer'
    #     else:
    #         self.folder['preffix'] = 'Consoles'


    #     self.folder['suffix'] = 'Translated-English'

    #     return self.folder

    # def get_path(self):
    #     self.get_folder()
    #     if self.get_company() != self.get_system():
    #         middle_path = os.path.join(self.get_company(), self.get_system())
    #     else:
    #         middle_path = self.get_system()

    #     self.path = os.path.join(*[x for x in [self.folder['preffix'], middle_path, self.folder['suffix']] if x])
    #     return self.path.strip()

    # def get_dat_path(self):
    #     if len('/'.split(self.get_path())) <= 2:
    #         return self.get_path()
    #     return os.path.dirname(self.get_path())

    def dict(self):
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

