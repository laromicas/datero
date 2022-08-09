from abc import ABC, abstractmethod
from operator import truediv
import shlex
import xmltodict
import re
from dateutil import parser


class Settings:
    UNION_CHARACTER = '-'
    Preffixes = {
        "Arcade": "Arcade",
        "Audio": "Other/Audio",
        "Book": "Other/Book",
        "Calculator": "Other/Calculator",
        "Computer": "Computer",
        "Console": "Consoles",
        "Handheld": "Consoles",
        "PDA": "Mobile",
        "Phone": "Mobile",
        "Source Code": "Other/Source Code",
        "Video": "Other/Video",
        "Mobile": "Mobile",
        "Manuals": "Other/Manuals",
        "BIOS Images": "Other/BIOS Images",
    }
    ROMVAULT_PATH = '/mnt/d/ROMVault'
    DAT_ROOT = f'{ROMVAULT_PATH}/DatRoot'
    OTHERDAT_ROOT = f'{ROMVAULT_PATH}/OtherDats'



def is_date(string, fuzzy=False):
    """
    Return whether the string can be interpreted as a date.

    :param string: str, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True
    """
    try:
        parser.parse(string, fuzzy=fuzzy)
        return True

    except ValueError:
        return False


class MyShas:
    shas = {}

    def add_rom(self, rom):
        self.shas[rom['@sha1'].lower()] = {
            'crc': rom['@crc'].lower(),
            'md5': rom['@md5'].lower(),
            'sha': rom['@sha1'].lower()
        }

    def check_rom(self, rom):
        checks = ['@sha1', '@md5', '@crc']
        for check in checks:
            if check in rom:
                return rom[check].lower() in self.shas


class DatDB:

    name = None

    def __init__(self, **kwargs) -> None:
        self.__dict__.update(kwargs)
        if not self.name:
            raise ValueError("No name specified")

    def load(self) -> None:
        pass

    def close(self) -> None:
        pass
