import os

# from packaging import version
import sys
from subprocess import DEVNULL, STDOUT, check_call

ROOT_FOLDER = os.path.dirname(sys.argv[0])
SEEDS_FOLDER = os.path.join(os.path.dirname(sys.argv[0]), 'seeds')


class Bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    def color_list():
        return [attr for attr in Bcolors.__dict__ if not callable(getattr(Bcolors, attr)) and not attr.startswith("__")]

    def no_color():
        for color in Bcolors.color_list():
            setattr(Bcolors, color, '')

def quiet_mode(command):
    command = command.split(' ')
    check_call(command, stdout=DEVNULL, stderr=STDOUT)

class ExecuteCommand:
    stdout = DEVNULL
    stderr = STDOUT

    def __init__(self, command):
        self.command = command

    def execute(command):
        check_call(command, stdout=ExecuteCommand.stdout, stderr=ExecuteCommand.stderr)