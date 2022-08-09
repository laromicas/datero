import json
from pydoc import locate
import importlib
import os
import sys

if not os.getcwd() in sys.path:
    sys.path.append(os.getcwd())

from lib.database.models.datfile import Dat

ROMVAULT_PATH = '/mnt/d/ROMVault'

class Processor:
    _previous = None

    def __init__(self, **kwargs):
        self._previous = None
        self.repo = 'redump'
        self.file = '/mnt/i/E/ROMVault/UpdateDats/tmp/redump/dats/bios/Microsoft - Xbox - BIOS Datfile (7) (2010-09-13).dat'
        self.actions = [
            {
                'action': 'LoadDatFile',
                'class_name': 'lib.repos.redump.redump_dat.RedumpBiosDat'
            },
            {
                'action': 'DeleteOld'
            },
            {
                'action': 'Copy'
            },
            {
                'action': 'SaveToDatabase'
            }
        ]
        self.__dict__.update(kwargs)

    def process(self):
        for action in self.actions:
            action_class = globals()[action['action']](file=self.file, repo=self.repo, previous=self._previous, **action)
            action_class.process()
            self._previous = action_class.output

        # return self.action(self.data)


class LoadDatFile:
    output = None
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self._class = locate(self.class_name)

    def process(self):
        self._dat = self._class(file=self.file)
        self._dat.load()
        # self._dat.parse()
        self.database = Dat(repo=self.repo, **self._dat.dict())
        self.output = self.database.dict()

class DeleteOld:
    output = None
    previous = None

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        pass

    def process(self):
        self.database = Dat(repo=self.previous['repo'], name=self.previous['name'])
        self.database.load()
        olddat = self.database.dict()
        if 'new_file' in olddat and os.path.exists(olddat['new_file']):
            os.unlink(self.database.dict()['new_file'])

        self.output = self.previous

class Copy:
    output = None
    previous = None
    destination = None
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        pass

    def process(self):
        if self.file:
            origin = self.file
        filename = os.path.basename(origin)
        self.destination = self.destination if self.destination else self.previous['path']
        destination = os.path.join(ROMVAULT_PATH, self.folder, self.destination, filename)
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        os.system(f'cp "{origin}" "{destination}"')
        if self.previous:
            self.previous['new_file'] = destination
        self.output = self.previous


class SaveToDatabase:
    output = None
    previous = None

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def process(self):
        self.database = Dat(**self.previous)
        self.database.save()
        self.database.close()

if __name__ == '__main__':
    procesor = Processor()
    procesor.process()