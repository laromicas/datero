from typing import Optional
from pydantic import BaseModel, Extra
from tinydb import Query, TinyDB
from tinydb.table import Table
from lib.database import DB


class Database(object):
    DB = DB
    table = None


class DatabaseModel(BaseModel):
    class Config:
        extra = Extra.allow
        arbitrary_types_allowed = True

    _DB = Database()
    _id: int = None
    _table_name: str = None

    def __init__(self, **kwargs) -> None:
        self._DB.DB = DB
        self._DB.table = DB.table(self._table_name)
        super().__init__(**kwargs)

    def load(self):
        result = self._DB.table.search(self.query())
        if result:
            self.__dict__.update(result[0])


    def save(self):
        query = Query()
        if self._id:
            self._DB.table.upsert(self.dict(), query.id == self._id)
        else:
            self._id = self._DB.table.upsert(self.dict(), self.query())

    def query(self):
        query = Query()
        return query.id == self._id

    def close(self):
        self._DB.table.storage.flush()



class Dat(DatabaseModel):
    _table_name = 'dats'
    name: str
    modifier: Optional[str]
    company: Optional[str]
    system: Optional[str]
    repo: str

    def query(self):
        query = Query()
        return (query.name == self.name) & (query.repo == self.repo)


class Repo(DatabaseModel):
    _table_name = 'repos'
    name: str

    def query(self):
        query = Query()
        return query.name == self.name

class System(DatabaseModel):
    _table_name = 'systems'
    company: Optional[str]
    system: str

    def query(self):
        query = Query()
        return (query.company == self.company) & (query.system == self.system)
