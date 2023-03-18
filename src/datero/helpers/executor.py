import logging
from subprocess import PIPE, CalledProcessError, Popen
from datero.configuration import config

class Command:
    """ Subprocess wrapper """
    quiet = config.getboolean('COMMAND', 'Quiet', fallback=False)
    verbose = config.getboolean('COMMAND', 'Verbose', fallback=False)
    logging = config.getboolean('LOG', 'Logging', fallback=False)
    logfile = config.get('LOG', 'LogFile', fallback='datero.log')

    def __init__(self, command):
        self.command = command

    # def execute(args, bufsize=- 1, executable=None, stdin=None, stdout=None, stderr=None, preexec_fn=None, close_fds=True, shell=False, cwd=None, env=None, universal_newlines=None, startupinfo=None, creationflags=0, restore_signals=True, start_new_session=False, pass_fds=(), group=None, extra_groups=None, user=None, umask=- 1, encoding=None, errors=None, text=None, pipesize=- 1, process_group=None): popen
    def execute(args, cwd=None, env=None, universal_newlines=True, shell=False):
        def execute(args):
            popen = Popen(args, stdout=PIPE, universal_newlines=universal_newlines, cwd=cwd, env=env, shell=shell)
            for stdout_line in iter(popen.stdout.readline, ""):
                yield stdout_line
            popen.stdout.close()
            return_code = popen.wait()
            if return_code:
                raise CalledProcessError(return_code, args)

        for output in execute(args):
            # print(output, end="")
            logging.info(output)
