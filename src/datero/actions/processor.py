"""
Process actions.
"""
# pylint: disable=too-few-public-methods
import os
from pydoc import locate
from datero.commands import config
from datero.database.models.datfile import Dat


class Processor:
    """ Process actions. """
    _previous = None
    actions = []
    seed = None
    file = None

    def __init__(self, **kwargs):
        self._previous = None
        self.__dict__.update(kwargs)

    def process(self):
        """ Process actions. """
        for action in self.actions:
            action_class = globals()[action['action']](file=self.file, seed=self.seed, previous=self._previous, **action)
            yield action_class.process()
            self._previous = action_class.output


class Process:
    """ Process Base class. """
    output = None
    status = None
    previous = {}
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

class LoadDatFile(Process):
    """ Load a dat file. """
    class_name = None
    file = None
    seed = None
    database = None
    _class = None
    _dat = None

    def process(self):
        """ Load a dat file. """
        self._class = locate(self.class_name)
        self._dat = self._class(file=self.file)
        self._dat.load()
        self.database = Dat(seed=self.seed, **self._dat.dict())
        self.output = self.database.dict()
        return "Loaded"


class DeleteOld(Process):
    """ Delete old dat file. """
    database = None
    def process(self):
        """ Delete old dat file. """
        self.database = Dat(seed=self.previous['seed'], name=self.previous['name'])
        self.database.load()
        olddat = self.database.dict()
        if 'new_file' in olddat and olddat['new_file'] and os.path.exists(olddat['new_file']):
            os.unlink(olddat['new_file'])

        self.output = self.previous
        return "Deleted"


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

        destination = os.path.join(config.get('PATHS','RomVaultPath'), self.folder, self.destination, filename)
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        result = None
        if self.previous:
            self.database = Dat(seed=self.previous['seed'], name=self.previous['name'])
            self.database.load()
            if self.database.is_enabled():
                old_file = self.database.dict().get('new_file', '')
                new_file = destination
                if old_file != new_file or config['GENERAL']['Overwrite'] or not os.path.exists(destination):
                    if old_file != new_file:
                        result = "Updated"
                    elif config['GENERAL']['Overwrite']:
                        result = "Overwritten"
                    self.previous['new_file'] = destination
                    os.system(f'cp "{origin}" "{destination}"')
            else:
                self.previous['new_file'] = None
                result = "Ignored"
        else:
            os.system(f'cp "{origin}" "{destination}"')
            result = "Copied"

        self.output = self.previous
        return result or "Copied"


class SaveToDatabase(Process):
    """ Save process to database. """
    database = None
    def process(self):
        """ Save process to database. """
        self.database = Dat(**self.previous)
        self.database.save()
        self.database.close()
        return "Saved"


if __name__ == '__main__':
    procesor = Processor()
    procesor.process()
