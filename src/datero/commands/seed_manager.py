import logging
import os
import sys
from . import ROOT_FOLDER, SEEDS_FOLDER, Command


def read_seed_repositories():
    with open(os.path.join(ROOT_FOLDER, 'seeds.txt'), 'r') as seeds:
        for seed in seeds:
            seed = seed.strip().split(' ')
            yield (seed[0], seed[1], ' '.join(seed[2:]) if len(seed) > 2 else '')


def get_seed_repository(seed_needed):
    with open(os.path.join(ROOT_FOLDER, 'seeds.txt'), 'r') as seeds:
        for seed in seeds:
            seed = seed.strip().split(' ')
            if seed[0] == seed_needed:
                return seed[1]
    return None


def seed_available():
    for seed in read_seed_repositories():
        yield seed[0], seed[2]


def seed_install(args, repository):
    repository = repository if repository.startswith('http') else 'https://' + repository
    repository = repository[:-4] if repository.endswith('.git') else repository
    branch = args.branch if getattr(args, 'branch', None) else 'master'
    url = os.path.join(repository, 'archive', f'{branch}.zip')
    path = os.path.join(SEEDS_FOLDER, args.seed)
    os.system(f'rm -rf {path}')
    Command.execute(['wget', f'{url}', '-O', f'datero_{args.seed}-{branch}.zip', '-c'], cwd=SEEDS_FOLDER)
    Command.execute(['unzip', f'datero_{args.seed}-{branch}.zip'], cwd=SEEDS_FOLDER)
    os.unlink(os.path.join(SEEDS_FOLDER, f'datero_{args.seed}-{branch}.zip'))
    os.rename(os.path.join(SEEDS_FOLDER, f'datero_{args.seed}-{branch}'), os.path.join(SEEDS_FOLDER, args.seed))
    if args.install_dependencies:
        seed_install_dependencies(args.seed)


def seed_remove(seed):
    path = os.path.join(SEEDS_FOLDER, seed)
    os.system(f'rm -rf {path}')


def seed_install_dependencies(seed):
    def install(package):
        output = io.StringIO()
        sys.stdout = sys.stderr = output
        if hasattr(pip, 'main'):
            pip.main(['install', package])
        else:
            pip._internal.main(['install', package])
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        logging.info(output.getvalue())

    if os.path.exists(os.path.join(SEEDS_FOLDER, seed, 'requirements.txt')):
        import pip
        import io
        with open(os.path.join(SEEDS_FOLDER, seed, 'requirements.txt'), 'r') as requirements:
            for requirement in requirements:
                install(requirement)
