"""
Helpers
"""

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
    from dateutil import parser
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

def is_git_path(path):
    """ Check if a path is a git repository. """
    import re
    pattern = re.compile((r"((git|ssh|http(s)?)|(git@[\w\.]+))(:(//)?)([\w\.@\:/\-~]+)(\.git)(/)?"))
    return pattern.match(path)

def is_git_repo(path):
    """ Check if a path is a git repository. """
    import os
    if os.path.isdir(os.path.join(path, ".git")):
        return True
    return False