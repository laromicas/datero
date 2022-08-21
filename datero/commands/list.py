import os
from . import SEEDS_FOLDER, Bcolors

def installed_seeds():
    for seed in os.listdir(SEEDS_FOLDER):
        if not os.path.isdir(os.path.join(SEEDS_FOLDER, seed)):
            continue
        name = seed
        description = seed_description(seed)
        yield (name, description)

def seed_description(seed):
    description = ''
    if os.path.isfile(os.path.join(SEEDS_FOLDER, seed, 'description.txt')):
        with open(os.path.join(SEEDS_FOLDER, seed, 'description.txt'), 'r') as desc:
            description = desc.readline().strip()
    return description
