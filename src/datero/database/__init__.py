"""
    Database module
"""
import os

from typing import Dict, Any
from tinydb import TinyDB, JSONStorage
from tinydb.middlewares import CachingMiddleware

from datero.configuration import config


os.makedirs(f"{os.path.join(os.getcwd(), config.get('PATHS','DatabasePath'))}", exist_ok=True)

DATABASE_URL = f"{config.get('PATHS','DatabasePath')}/{config.get('PATHS','DatabaseFile')}"

class JSONStorageWithBackup(JSONStorage):
    """ TinyDB JSON storage with backup. """
    path: str = DATABASE_URL

    def __init__(self, path: str, create_dirs=False, encoding=None, access_mode='r+', **kwargs):
        self.path = path
        super().__init__(path, create_dirs, encoding, access_mode, **kwargs)

    def write(self, data: Dict[str, Dict[str, Any]]):
        """ Write data to the storage. """
        self.make_backup()
        super().write(data)

    def make_backup(self):
        """ Make a backup of the database. """
        os.system(f"cp {self.path} {self.path}.bak")


DB = TinyDB(DATABASE_URL, storage=CachingMiddleware(JSONStorageWithBackup))

# DB = TinyDB(DATABASE_URL, storage=JSONStorageWithBackup, indent=4)
