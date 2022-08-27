import os
import configparser

from .. import ROOT_FOLDER

config = configparser.ConfigParser(allow_no_value=True)
config.optionxform = lambda option: option
config.read(os.path.join(ROOT_FOLDER, 'datero.ini'))
config.read(os.path.join(os.getcwd(), '.daterorc'))
