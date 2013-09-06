#!/usr/bin/python

from sys import stdout, stderr, exit

QUIET = 0
NORMAL = 1
DEBUG = 2

class Output(object):
    def __init__(self, verbosity=NORMAL, outfile='/dev/null'):
        self.verbosity = verbosity
        self.outfile = self.setOutFile(outfile)
        self._stdout = stdout
        self._stderr = stderr

    def setOutFile(self, outfile):
        self._writer = open(outfile, 'a')

    def _write(self, msg, level='INFO', exit_code=None):
        if self.verbosity == QUIET:
            return
        if isinstance(msg, (tuple)):
            msg, exit_code = msg
        if level != 'INFO':
            msg = '{0}: {1}'.format(level,msg)
        msg = '{0}\n'.format(msg)
        self._writer.write(msg)
        self._writer.flush()
        if level in ('ERROR', 'CRITICAL'):
            self._stderr.write(msg)
            self._stderr.flush()
        else:
            self._stdout.write(msg)
            self._stdout.flush()
        if exit_code is not None:
            exit(exit_code)

    def info(self, msg):
        self._write(msg)

    def debug(self, msg, name=None, **kwargs):
        if self.verbosity != DEBUG:
            return
        title = kwargs.get('title', None)
        if name is not None:
            msg = '{0} = {1}'.format(name, msg)
        elif title is not None:
            msg = '{0} {1}'.format(title, msg)
        self._write(msg, 'DEBUG')

    def warning(self, msg):
        self._write(msg, 'WARNING')

    def error(self, msg, exit_code=None):
        self._write(msg, 'ERROR', exit_code)

    def critical(self, msg, exit_code=None):
        self._write(msg, 'CRITICAL', exit_code)

    def _test(self, msg='this is a test'):
        self.info(msg)
        self.debug(msg)
        self.warning(msg)
        self.error(msg)
        self.critical(msg)

if __name__ == '__main__':
    for level in (QUIET,NORMAL,DEBUG):
        print "Testing verbosity level {}".format(level)
        a = Output(level)
        a._test()
        print
