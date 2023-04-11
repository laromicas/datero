import os
from pydoc import locate
from datero.database.models.datfile import Dat
from datero.repositories.dat import DatFile, XMLDatFile, ClrMameProDatFile
from datero.seeds.rules import Rules
from datero.seeds.unknown_seed import detect_seed

class Merge:
    """ Merge two dat files. """

    child = {}
    parent = {}

    def __init__(self, child, parent=None):
        self.child = {}
        self.parent = {}

        def load_metadata(var, obj):
            if isinstance(var, str):
                if ':' in var:
                    splitted = var.split(':')
                    seed = splitted[0]
                    name = splitted[1]
                    obj['db'] = Dat(name=name, seed=seed)
                    obj['db'].load()
                    var = obj['db']
                elif var.endswith('.dat') or var.endswith('.xml'):
                    obj['file'] = var
                else:
                    raise Exception("Invalid dat file")
            if isinstance(var, Dat):
                obj['db'] = var
                obj['file'] = getattr(var, 'new_file', None) or var.file
            if isinstance(var, DatFile):
                obj['dat'] = var
            else:
                obj['dat'] = self.get_dat_file(obj['file'])

        load_metadata(child, self.child)
        if not parent:
            parent = self.child['db'].parent
        load_metadata(parent, self.parent)

    def get_dat_file(self, file):
        try:
            dat = XMLDatFile(file=file)
            dat.load()
            return dat
        except Exception:
            pass
        try:
            dat = ClrMameProDatFile(file=file)
            dat.load()
            return dat
        except Exception:
            pass
        raise Exception("Invalid dat file")

    def dedupe(self):
        self.child['dat'].merge_with(self.parent['dat'])
        return self.child['dat']

    def save(self):
        self.child['dat'].save()