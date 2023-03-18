import json
import os
from pathlib import Path
from pydoc import locate
from datero.configuration import config
from datero.commands import SEEDS_FOLDER
from datero.commands.seed_manager import seed_available
from datero.repositories.dat import ClrMameProDatFile, XMLDatFile


def detect_seed(dat_file: str, rules_classes):
    """ Detect the seed for a dat file. """
    try:
        dat = XMLDatFile(file=dat_file)
        for rule_class in rules_classes:
            found = True
            # print(dat.header)
            for rule in rule_class['rules']:
                # print(rule['key'], rule['value'], rule['operator'])
                if not comparator(dat.header.get(rule['key']), rule['value'], rule['operator']):
                    found = False
                    break
            if found:
                return rule_class['class_name']
    except Exception:
        try:
            dat = ClrMameProDatFile(file=dat_file)
            found = True
            for rule_class in rules_classes:
                for rule in rule_class['rules']:
                    if not comparator(dat.header.get(rule['key']), rule['value'], rule['operator']):
                        found = False
                        break
                if found:
                    return rule_class['class_name']
        except Exception:
            pass

def comparator(key, value, operator):
    """ Returns a boolean based on the comparison of the key and value. """
    match operator:
        case 'eq' | 'equals' | '==':
            return key == value
        case 'ne' | 'not_equals' | '!=':
            return key != value
        case 'gt' | 'greater_than' | '>':
            return key > value
        case 'lt' | 'less_than' | '<':
            return key < value
        case 'ge' | 'greater_than_or_equals' | '>=':
            return key >= value
        case 'le' | 'less_than_or_equals' | '<=':
            return key <= value
        case 'in' | 'is_contained_in' | 'has':
            return key in value
        case 'ni' | 'not_in' | 'is_not_contained_in' | 'hasnt' | 'has_not':
            return key not in value
        case 're' | 'regex' | 'matches' | 'match' | 'matches_regex' | 'match_regex':
            return re.search(value, key)
        case 'nr' | 'not_regex' | 'not_matches' | 'not_match' | 'not_matches_regex' | 'not_match_regex':
            return not re.search(value, key)
        case 'sw' | 'starts_with':
            return key.startswith(value)
        case 'ew' | 'ends_with':
            return key.endswith(value)
        case 'ns' | 'not_starts_with':
            return not key.startswith(value)
        case 'ne' | 'not_ends_with':
            return not key.endswith(value)
        case 'co' | 'contains':
            return value in key
        case 'nc' | 'not_contains':
            return value not in key
        case 'ex' | 'exists':
            return bool(key)
        case 'nx' | 'not_exists' | 'not_exist' | 'not_exits' | 'not_exits':
            return not bool(key)
        case 'bt' | 'between' | 'in_range' | 'in_between':
            return value[0] <= key <= value[1]
        case 'nb' | 'not_between' | 'not_in_range' | 'not_in_between':
            return not (value[0] <= key <= value[1])
        case 'is':
            return key is value
        case 'isnt' | 'is_not':
            return key is not value
    return False





#     path = config['PATHS']['DatPath']
#     dats = { str(x):"" for x in Path(path).rglob("*.[dD][aA][tT]") }
#     print(dats)

#     # for dat in dat_list:
#         # print(dat)
#         # # dat_list.append(os.path.join(path, dat))
#         # for
#         # self._dat = self._class(file=self.file)

# def process_dats():
#     """ Detect the seed for a dat file. """
#     global classes, dats
#     load_dats()
#     print(classes)

#     path = config['PATHS']['DatPath']
#     dats = { str(x):"" for x in Path(path).rglob("*.[dD][aA][tT]") }
#     print(dats)
