# from lib.database import DB
# from tinydb import Query
from lib.database.models import System
import json
import requests

# rules = [
#     {
#         "key": "system",
#         "comparison": "=",
#         "value": "Pocket PC",
#         "fixed": {
#             "preffix": "Phone",
#             "company": "Microsoft"
#         }
#     },
#     {
#         "key": "system",
#         "comparison": "=",
#         "value": "Sony Electronic Book",
#         "fixed": {
#             "company": "Sony"
#         }
#     },
#     {
#         "key": "system",
#         "comparison": "=",
#         "value": "FM Towns",
#         "fixed": {
#             "preffix": "Computer",
#             "system": "FM-Towns"
#         }
#     },
#     {
#         "key": "system",
#         "comparison": "contains",
#         "value": "PC Compatible",
#         "fixed": {
#             "preffix": "Computer",
#             "system": "PC and Compatibles"
#         }
#     },
#     {
#         "key": "system",
#         "comparison": "contains",
#         "value": "GameCube",
#         "fixed": {
#             "system": "GameCube"
#         }
#     },
#     {
#         "key": "system",
#         "comparison": "contains",
#         "value": "Saturn",
#         "fixed": {
#             "system": "Saturn"
#         }
#     },
#     {
#         "key": "system",
#         "comparison": "contains",
#         "value": "Sega Mega CD",
#         "fixed": {
#             "system": "Mega CD & Sega CD"
#         },
#         "replaces": {
#             "format": ["&", "{UNION_CHARACTER}"],
#             "format": ["+", "{UNION_CHARACTER}"],
#         }
#     },
#     {
#         "key": "system",
#         "comparison": "in",
#         "value": ('Audio CD', 'BD-Video', 'DVD-Video', 'Video Game Magazine Scans'),
#         "fixed": {
#             "company": None,
#             }
#     },
#     {
#         "key": "system",
#         "comparison": "in",
#         "value": ('BD-Video', 'DVD-Video'),
#         "fixed": {
#             "company": None,
#             "preffix": "Other/Video",
#         }
#     },
#     {
#         "key": "system",
#         "comparison": "in",
#         "value": ('BD-Video', 'DVD-Video'),
#         "fixed": {
#             "company": None,
#             "preffix": "Other/Video",
#         }
#     },
#     {
#         "key": "system",
#         "comparison": "in",
#         "value": ('Video Game Magazine Scans'),
#         "fixed": {
#             "company": None,
#             "preffix": "Other/Manuals",
#         }
#     },
#     {
#         "key": "suffix",
#         "comparison": "in",
#         "value": ('UMD Music'),
#         "fixed": {
#             "system": None,
#             "preffix": "Other/Manuals",
#         }
#     },
# ]


fields = [
    'company',
    'system',
    'override',
    'extra_configs',
    'system_type',
]


def get_systems():
    result = requests.get('https://sheets.googleapis.com/v4/spreadsheets/1LgU7uJOtVOUWYkdoaeSbux41biFwpbzVosm98bgdN3k/values/Systems!A1:E300?key=AIzaSyA2pmHY5FVJFEjauoE8kKV6-UcCM4Tfk44')
    systems_result = result.json()['values']
    systems = []
    for i in range(1, len(systems_result)):
        system = systems_result[i]
        row = {}
        for j in range(len(fields)):
            field = fields[j]
            if len(system) > j and system[j] != '':
                row[field] = system[j]
            elif field == 'company':
                row[field] = None
            if field in ('override', 'extra_configs') and field in row:
                try:
                    row[field] = json.loads(system[j])
                except Exception as e:  # pylint: disable=broad-except
                    # print(e, system[j])
                    row[field] = system[j]
        systems.append(row)
    return systems


def __import__():
    systems = get_systems()
    for system in systems:
        row = System(**system)
        row.save()
