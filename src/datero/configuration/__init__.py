""" Configuration module """
__all__ = ['config', 'logger', 'ROOT_FOLDER']

import os
from datero import ROOT_FOLDER

from datero.configuration.configuration import config
from datero.configuration.logger import logger

SEEDS_FOLDER = os.path.join(ROOT_FOLDER, 'seeds')
