import os
import json
from typing import List, Union
from pathlib import Path
from pysondb.db import PysonDB
from pysondb.db_types import DBSchemaType
from pysondb.db_types import SingleDataType
from pysondb.db_types import QueryType


class MyJsonDatabase(PysonDB):
    """ An extension of PysonDB that can use indexes for faster access. """
    def __init__(self, filename: str, auto_update: bool = True, indent: int = 4) -> None:
        super().__init__(filename, auto_update, indent)
        if os.path.exists(filename):
            self.force_load()

    def _gen_db_file(self) -> None:
        self._au_memory: DBSchemaType = {'version': 3, 'keys': [], 'data': {}, 'indexes': {}}
        if self.auto_update:
            if not Path(self.filename).is_file():
                self.lock.acquire()
                self._dump_file(self._au_memory)
                self.lock.release()

    # Backup the database
    def make_backup(self) -> None:
        """ Creates a backup of the database. """
        if os.path.exists(self.filename):
            os.system(f'cp {self.filename} {self.filename}.bak')

    def _dump_file(self, data: DBSchemaType) -> None:
        """ Creates a backup of the database before writing to it. """
        self.make_backup()
        super()._dump_file(data)

    # Index management
    def create_index(self, index_field: str) -> None:
        self._au_memory['indexes'][index_field] = {}
        self._rebuild_index(index_field)

    def delete_index(self, index_field: str):
        if index_field in self._au_memory['indexes']:
            del self._au_memory['indexes'][index_field]

    def _rebuild_index(self, index_field: str):
        for key, item in self._au_memory['data'].items():
            if item[index_field] not in self._au_memory['indexes'][index_field]:
                self._au_memory['indexes'][index_field][item[index_field]] = {}
            self._au_memory['indexes'][index_field][item[index_field]][key] = item

    def _rebuild_indexes(self):
        if 'indexes' in self._au_memory:
            for index_field in self._au_memory['indexes']:
                self._rebuild_index(index_field)

    def _add_to_indexes(self, id: int, data: DBSchemaType):
        if 'indexes' in self._au_memory:
            for index_field in self._au_memory['indexes']:
                if index_field in data:
                    if data[index_field] not in self._au_memory['indexes'][index_field]:
                        self._au_memory['indexes'][index_field][data[index_field]] = {
                        }
                    self._au_memory['indexes'][index_field][data[index_field]][id] = data

    # Override and new data manipulation methods for indexing
    def add(self, data: DBSchemaType) -> int:
        id = super().add(data)
        self._add_to_indexes(id, data)
        return id

    def add_many(self, data: object, json_response: bool = False) -> Union[SingleDataType, None]:
        yield super().add_many(data, json_response)
        self._rebuild_indexes()

    def update_by_id(self, id: str, new_data: object) -> SingleDataType:
        id = super().update_by_id(id, new_data)
        self._add_to_indexes(id, new_data)
        return id

    def update_by_query(self, query: QueryType, new_data: object) -> List[str]:
        result = super().update_by_query(query, new_data)
        self._rebuild_indexes()
        return result

    # New methods for data retrieval
    def add_or_update(self, query, new_data):
        if self.get_by_query(query=query):
            self.update_by_query(query=query, new_data=new_data)
        else:
            self.add(new_data)


class SystemsDatabase(MyJsonDatabase):
    pass


class DatsDatabase(MyJsonDatabase):
    pass


class DatReposDatabase(MyJsonDatabase):
    pass


get_systems_db = SystemsDatabase
get_dats_db = DatsDatabase
get_dat_repos_db = DatReposDatabase
