#!/usr/bin/python

# Inherit from primary library
import atomhopper as ah
import atomhopper.auth as auth
from atomhopper.output import Output, QUIET, NORMAL, DEBUG

# Bring in libraries only relevant to the wrapper script
from optparse import OptionParser, OptionGroup
import configobj
import validate
import keyring
import os
import sys
from getpass import getpass

# Set using constants for output levels
VERBOSITY = NORMAL

# Set action constants
GET = 0
POST = 1

APP_NAME        = os.path.basename(sys.argv[0]).split('.')[0]
CONFIG_FILE    = '/etc/{0}.conf'.format(APP_NAME)
LOG_FILE       = '/var/log/{0}.log'.format(APP_NAME)
if not os.access(LOG_FILE, os.W_OK):
    LOG_FILE = '{0}.log'.format(APP_NAME)


DEFAULTS = {
    'endpoint': { 'type': 'string', 'default': ah.ENDPOINT },
    'timeout': { 'type': 'integer', 'min':60, 'max': 1800, 'default': 300 },
    'username': { 'type': 'string' },
    'token': { 'type': 'string' },
    'password': { 'type': 'string' },
    'keyring': { 'type': 'string' },
    'auth_endpoint': { 'type': 'string', 'default': auth.ENDPOINT },
    'log_file': { 'type': 'string', 'default': LOG_FILE },
}

def interactive_debug(type, value, tb):
    import ipdb, traceback
    traceback.print_exception(type, value, tb)
    ipdb.pm()

def convert_dict_to_spec(spec):
    newspec = []
    for opt, data in spec.iteritems():
        details = []
        if 'options' in data.keys():
            details.append("'{0}'".format("','".join(str(x) for x in data['options'])))
        for k,v in data.iteritems():
            if k in ['type','options']:
                continue
            if type in ['list','string_list'] and k == 'default':
                v = "list('{0}')".format("','".join(v))
            if isinstance(v, str):
                v = "'{0}'".format(v)
            details.append("{0}={1}".format(k,v))
        newspec.append('{0} = {1}({2})'.format(opt, data['type'], ",".join(details)))
    return newspec

def parse_config(path, spec=None):
    if spec:
        if isinstance(spec, str):
            spec = spec.split("\n")
        elif isinstance(spec, dict):
            spec = convert_dict_to_spec(spec)
    config = configobj.ConfigObj(path, configspec=spec)
    if spec:
        config.validate(validate.Validator(), copy=True)
    return config.dict()

def parse_opts_args():
    # Parser Configuration
    parser = OptionParser(usage='Usage: %s [options]')
    general = OptionGroup(parser, 'General')
    atom = OptionGroup(parser, 'Atom Hopper Instance')
    auth = OptionGroup(parser, 'Authentication')

    general.add_option('-c', '--config',
            help='Alternate path to look for the default config file'),
    general.add_option('-o', '--log-file',
            help='File to log output to.'),
    general.add_option('--debug', dest='verbosity',
            action='store_const', const=DEBUG,
            help='Enable debug output of script... a bit excessive usually'),
    general.add_option('--quiet', dest='verbosity',
            action='store_const', const=QUIET,
            help='Silence the output of the script, still logs to file'),
    general.add_option('-t', '--timeout', type='int',
            help='How long to wait for individual steps of process before erroring out a node'),
    atom.add_option('-e', '--endpoint',
            help='URL for the Atom Hopper feed')
    atom.add_option('--category',
            help='Category for classifying your post')
    atom.add_option('--post', dest='action', action='store_const', const=POST,
            help='Post an entry to the feed')
    auth.add_option('-u', '--username',
            help='Username to pass for authentication'),
    auth.add_option('-p', '--password', action="store_true", default=False,
            help='Prompt for password for authentication'),
    auth.add_option('--keyring',
            help='Which system keyring to pull password from'),
    auth.add_option('--token',
            help='Token for authentication.'),
    auth.add_option('--auth-endpoint',
            help='Define a specific auth endpoint url'),
    parser.add_option_group(general)
    parser.add_option_group(atom)
    parser.add_option_group(auth)
    # we'll handle remaining defaults when parsing CONFIG
    parser.set_defaults(config=CONFIG_FILE, verbosity=NORMAL)
    return parser.parse_args()

def get_config(defaults, options, output):
    # TODO validate inheritance 
    config = parse_config(options.config, defaults)
    config['log_file'] = defaults['log_file']
    config['verbosity'] = options.verbosity
    output.verbosity = config['verbosity']
    if output.outfile == LOG_FILE and 'log_file' in config:
        output.setOutFile(config['log_file'])
    output.debug(defaults, 'defaults', inspect=True)
    output.debug(config, 'config', inspect=True)
    for option, value in defaults.iteritems():
        if hasattr(options, option) and getattr(options, option):
            value = getattr(options, option)
            if value:
                output.debug(value, title="CLI override of %s" % (option))
                config[option] = value
        elif option not in config:
            output.debug(value, title="Default override of %s" % (option))
            config[option] = value
        else:
            output.warning('This should not have happened (%s)' % (option))
            output.debug(value, option)
    output.debug(config, 'config', inspect=True)
    return config

def get_config_and_output():
    (options, args) = parse_opts_args()
    debug = False
    if options.verbosity == DEBUG:
        debug = True
        sys.excepthook = interactive_debug
    log_file = LOG_FILE
    if options.log_file:
        log_file = options.log_file
    output = Output(options.verbosity, log_file)
    if not options.config:
        options.config = CONFIG_FILE
        output.debug(options.config, 'options.config')

    config = get_config(DEFAULTS, options, output)
    if options.keyring:
        config['password'] = keyring.get_password(options.keyring, options.user)
    elif options.password:
        config['password'] = getpass('Password: ')
    
    output.debug(config, 'config', inspect=True)
    return (config, output)
    
def run():
    (output, config) = get_config_and_output()
    feed = AtomFeed(**config)
    entry = AtomEntry('testing', __author__, __author_email__, content)
    print entry.renger()
    