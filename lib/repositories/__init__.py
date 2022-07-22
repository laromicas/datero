from email.policy import default
import os
from decouple import config
from . import db


SYSTEMS_URL = f"{config('DATABASE_PATH', default='database')}/{config('SYSTEMS_DB', default='systems.json')}"
DATS_URL = f"{config('DATABASE_PATH', default='database')}/{config('DATS_DB', default='dats.json')}"
REPOS_URL = f"{config('DATABASE_PATH', default='database')}/{config('REPOS_DB', default='datrepos.json')}"

# print(SYSTEMS_URL)
# print(DATS_URL)
# print(REPOS_URL)

systems_db = db.SystemsDatabase(SYSTEMS_URL)
dats_db = db.DatsDatabase(DATS_URL)
repos_db = db.DatReposDatabase(REPOS_URL, auto_update=False)
