import os
import sys
from subprocess import PIPE, DEVNULL, STDOUT, CalledProcessError, run
import configparser
from dateutil import parser


ROOT_FOLDER = os.path.dirname(sys.argv[0])
SEEDS_FOLDER = os.path.join(os.path.dirname(sys.argv[0]), 'seeds')

config = configparser.ConfigParser()
config.read(os.path.join(ROOT_FOLDER, 'datero.ini'))
config.read(os.path.join(os.getcwd(), '.daterorc'))

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

def is_date(string, fuzzy=False):
    """
    Return whether the string can be interpreted as a date.

    :param string: str, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True
    """
    try:
        parser.parse(string, fuzzy=fuzzy)
        return True

    except ValueError:
        return False


def sizeof_fmt(num, suffix="B"):
    """ Convert bytes to human readable format. """
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num: .1f}Yi{suffix}"


class Command:
    """ Subprocess wrapper """
    quiet = config.getboolean('COMMAND','Quiet', fallback=False)
    verbose = config.getboolean('COMMAND','Verbose', fallback=False)
    logging = config.getboolean('LOG','Logging', fallback=False)
    logfile = config.get('LOG','LogFile', fallback='datero.log')

    def __init__(self, command):
        self.command = command

    def quiet(quiet=True):
        Command.quiet = quiet
        Command.verbose = not quiet

    def verbose(verbose=True):
        Command.verbose = verbose
        Command.quiet = not verbose

    def logging():
        # TODO: add logging
        pass

    def execute(command, stdin=None, input=None, stdout=PIPE, stderr=STDOUT, capture_output=False, shell=False, cwd=None, timeout=None, check=False, errors=None, env=None, text=None):
        # print(shell)
        # check_call(command, stdout=ExecuteCommand.stdout, stderr=ExecuteCommand.stderr)
        #  subprocess.run(args, *, stdin=None, input=None, stdout=None, stderr=None, capture_output=False, shell=False, cwd=None, timeout=None, check=False, encoding=None, errors=None, text=None, env=None, universal_newlines=None, **other_popen_kwargs)
        # try:
        result = run(command, stdin=stdin, input=input, stdout=stdout, stderr=stderr, capture_output=capture_output, shell=shell, cwd=cwd, timeout=timeout, check=check, errors=errors, env=env, text=text)
        output = result.stdout.decode('unicode_escape')
        # except CalledProcessError as e:
        #     if not Command.quiet:
        #         print(output)

        #     return e.returncode

        if not Command.quiet:
            print(output)
        if Command.logging:
            pass
        return result.returncode
        # run(command, shell=shell)

        #  subprocess.check_call(args, *, stdin=None, stdout=None, stderr=None, shell=False, cwd=None, timeout=None, **other_popen_kwargs)
        #  Run command with arguments. Wait for command to complete. If the return code was zero then return, otherwise raise CalledProcessError.
        #
        #
        #  subprocess.check_output(args, *, stdin=None, stderr=None, shell=False, cwd=None, encoding=None, errors=None, universal_newlines=None, timeout=None, text=None, **other_popen_kwargs)
        #  Run command with arguments and return its output
        #  run(..., check=True, stdout=PIPE).stdout