"""
Process actions.
"""
# pylint: disable=too-few-public-methods
import os
from pydoc import locate
from lib import Settings
from lib.database.models.datfile import Dat


class Processor:
    """ Process actions. """
    _previous = None
    actions = []
    repo = None
    file = None

    def __init__(self, **kwargs):
        self._previous = None
        self.__dict__.update(kwargs)

    def process(self):
        """ Process actions. """
        for action in self.actions:
            action_class = globals()[action['action']](file=self.file, repo=self.repo, previous=self._previous, **action)
            action_class.process()
            self._previous = action_class.output


class Process:
    """ Process Base class. """
    output = None
    previous = {}
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

class LoadDatFile(Process):
    """ Load a dat file. """
    class_name = None
    file = None
    repo = None
    database = None
    _class = None
    _dat = None

    def process(self):
        """ Load a dat file. """
        self._class = locate(self.class_name)
        self._dat = self._class(file=self.file)
        self._dat.load()
        self.database = Dat(repo=self.repo, **self._dat.dict())
        self.output = self.database.dict()


class DeleteOld(Process):
    """ Delete old dat file. """
    database = None
    def process(self):
        """ Delete old dat file. """
        self.database = Dat(repo=self.previous['repo'], name=self.previous['name'])
        self.database.load()
        olddat = self.database.dict()
        if 'new_file' in olddat and os.path.exists(olddat['new_file']):
            os.unlink(olddat['new_file'])

        self.output = self.previous


class Copy(Process):
    """ Copy files. """
    destination = None
    file = None
    folder = None
    database = None

    def process(self):
        """ Copy files. """
        if self.file:
            origin = self.file
        filename = os.path.basename(origin)
        self.destination = self.destination if self.destination else self.previous['path']

        destination = os.path.join(Settings.ROMVAULT_PATH, self.folder, self.destination, filename)
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        if self.previous:
            self.database = Dat(repo=self.previous['repo'], name=self.previous['name'])
            self.database.load()
            if self.database.is_enabled():
                old_file = os.path.basename(self.database.dict()['new_file'])
                new_file = os.path.basename(destination)
                if old_file != new_file or Settings.Overwrite or not os.path.exists(destination):
                    self.previous['new_file'] = destination
                    os.system(f'cp "{origin}" "{destination}"')
            else:
                self.previous['new_file'] = None
        else:
            os.system(f'cp "{origin}" "{destination}"')

        self.output = self.previous


class SaveToDatabase(Process):
    """ Save process to database. """
    database = None
    def process(self):
        """ Save process to database. """
        self.database = Dat(**self.previous)
        self.database.save()
        self.database.close()


if __name__ == '__main__':
    procesor = Processor()
    procesor.process()
