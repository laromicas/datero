import os
from typing import Dict, Any
from tinydb import TinyDB, JSONStorage
from decouple import config

from unittest import mock

from tinydb.middlewares import CachingMiddleware

os.makedirs(f"{os.path.join(os.getcwd(), config('DATABASE_PATH', default='database'))}", exist_ok=True)

DATABASE_URL = f"{config('DATABASE_PATH', default='database')}/{config('DATABASE_URL', default='database.json')}"

class JSONStorageWithBackup(JSONStorage):
    path: str = DATABASE_URL

    def __init__(self, path: str, create_dirs=False, encoding=None, access_mode='r+', **kwargs):
        self.path = path
        super().__init__(path, create_dirs, encoding, access_mode, **kwargs)

    def write(self, data: Dict[str, Dict[str, Any]]):
        self.make_backup()
        super().write(data)

    def make_backup(self):
        os.system(f"cp {self.path} {self.path}.bak")


DB = TinyDB(DATABASE_URL, storage=CachingMiddleware(JSONStorageWithBackup), indent=4)

# DB = TinyDB(DATABASE_URL, storage=JSONStorageWithBackup, indent=4)
