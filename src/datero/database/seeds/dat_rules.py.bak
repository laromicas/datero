"""
    Seed the database with Systems.
"""
import json
import requests
from lib import Settings
from lib.database.models import System

fields = [
    'company',
    'system',
    'override',
    'extra_configs',
    'system_type',
]


def get_systems():
    """ Get systems from the Google Sheets. """
    result = requests.get(Settings.GOOGLE_SHEET_URL)
    systems_result = result.json()['values']
    systems = []
    for i in range(1, len(systems_result)):
        system = systems_result[i]
        row = {}
        for j, field in enumerate(fields):
            if len(system) > j and system[j] != '':
                row[field] = system[j]
            elif field == 'company':
                row[field] = None
            if field in ('override', 'extra_configs') and field in row:
                try:
                    row[field] = json.loads(system[j])
                except Exception:  # pylint: disable=broad-except
                    row[field] = system[j]
        systems.append(row)
    return systems


def _import_():
    """ Seed the database with Systems. """
    systems = get_systems()
    for system in systems:
        row = System(**system)
        row.save()
