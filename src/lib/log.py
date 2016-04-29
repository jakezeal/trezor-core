import sys
import utime

NOTSET = const(0)
DEBUG = const(10)
INFO = const(20)
WARNING = const(30)
ERROR = const(40)
CRITICAL = const(50)

_leveldict = {
    DEBUG: ('DEBUG', '32'),
    INFO: ('INFO', '36'),
    WARNING: ('WARNING', '33'),
    ERROR: ('ERROR', '31'),
    CRITICAL: ('CRITICAL', '1;31'),
}

level = NOTSET
color = True

def _log(name, mlevel, msg, *args):
    if __debug__ and mlevel >= level:
        if color:
            fmt = '%d \x1b[35m%s\x1b[0m %s \x1b[' + _leveldict[mlevel][1] + 'm' + msg + '\x1b[0m'
        else:
            fmt = '%d %s %s ' + msg
        print(fmt % ((utime.ticks_us(), name, _leveldict[mlevel][0]) + args), file=sys.stderr)

def debug(name, msg, *args):
    _log(DEBUG, msg, *args)

def info(name, msg, *args):
    _log(INFO, msg, *args)

def warning(name, msg, *args):
    _log(WARNING, msg, *args)

def error(name, msg, *args):
    _log(ERROR, msg, *args)

def critical(name, msg, *args):
    _log(CRITICAL, msg, *args)