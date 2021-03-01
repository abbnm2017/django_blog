#!/usr/bin/env python
import os
import sys
import signal


def signal_func():
    pass

def _setDaemon():
    global _bDaemon
    _bDaemon = True
   # directory = "/home/test/"
  #  if not os.path.exists(directory):
  #      os.mkdir(directory)

 #   os.chdir(directory)
    os.umask(0)
    try:
        pid = os.fork()
        if pid > 0:
            os._exit(0)
    except OSError:
        raise

    os.setsid()
    signal.signal(signal.SIGTERM, signal_func)
    signal.signal(signal.SIGINT, signal_func)
    signal.signal(signal.SIGQUIT, signal_func)
    signal.signal(signal.SIGHUP, signal_func)
    signal.signal(signal.SIGPIPE, signal_func)

    os.close(sys.stdin.fileno())
    os.close(sys.stdout.fileno())
    os.close(sys.stderr.fileno())

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    execute_from_command_line(sys.argv)
