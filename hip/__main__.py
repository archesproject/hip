import argparse
import codecs
import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hip.settings")
here = os.path.abspath(os.path.dirname(__file__))
COMMANDS = {}

def get_arches_env():
    with codecs.open(os.path.join(here, '..', 'Procfile'), 'r', encoding='utf-8-sig') as f: 
        for line in f:
            if 'django:' in line:
                return line.replace('django:', '').strip().split(' ')[0].strip()

# ACIVATE THE VIRTUAL ENV
path_to_virtual_env = get_arches_env()
if sys.platform == 'win32':
    activate_this = os.path.normpath(os.path.join(path_to_virtual_env, '..', 'activate_this.py'))
else:
    activate_this = os.path.normpath(os.path.join(path_to_virtual_env, '..', 'activate_this.py'))
execfile(activate_this, dict(__file__=activate_this))

from arches.management.commands import utils
#from hip import version

try:
    # Python 3
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer)
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.buffer)
except AttributeError:
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout)
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr)


class CommandError(Exception):
    pass

parent_parser = argparse.ArgumentParser(add_help=False)
# parent_parser.add_argument(
#     '-v', '--version',
#     action='version', version='%(prog)s' + ' Version %s : Build %s' % (version.__VERSION__, version.__BUILD__))

parser = argparse.ArgumentParser(
    prog='hip', 
    description='Manage Arches-based Applications',
    parents=[parent_parser], 
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

subparsers = parser.add_subparsers(title='available commands', dest='command')
subparsers.required = True


def command_run_es(args):
    os.system('%s %s packages -o start_elasticsearch"' % (path_to_virtual_env, os.path.normpath(os.path.join(here, '..', 'manage.py'))))

parser_start = subparsers.add_parser(
    'runsearchengine',
    help="Starts the elasticsearch process",
)
COMMANDS['runsearchengine'] = command_run_es


def command_runserver(args):
    os.system('%s %s runserver %s"' % (path_to_virtual_env, os.path.normpath(os.path.join(here, '..', 'manage.py')), args.port))

parser_start = subparsers.add_parser(
    'runserver',
    help="Starts the elasticsearch process",
)
parser_start.add_argument(
    '-p', '--port',
    help="port to run the django dev server on, defaults to 8000",
    type=str, 
    default=8000,
)
COMMANDS['runserver'] = command_runserver


def command_load(args):
    filename = 'data_paths.txt'
    path_to_file = os.path.join(here, filename)
    path = None
    keyfound = False
    errortext = None
    content = None
    items = {}

    try:
        if args.path:
            # don't let someone add a bad path
            args.path = os.path.abspath(args.path)
            if not os.path.exists(args.path):
                raise Exception('ERROR: path (%s) doesn\'t exist' % (args.path))
        if args.name:
            if os.path.isfile(path_to_file):
                with codecs.open(path_to_file, 'r', encoding='utf-8-sig') as f: 
                    for row in f:
                        key = row.split(':')[0]
                        value = ':'.join(row.split(':')[1:])
                        items[key] = value

                        if key == args.name:
                            keyfound = True
                            if args.path: # user is updating path
                                items[key] = args.path 
                                path = args.path
                            else:
                                path = value
                    
                    if not keyfound and not args.path:
                        raise Exception('ERROR: the name "%s" you referenced in the command doesn\'t exist. Did you forget to add a path?' % (args.name))
            else:
                if args.path:
                    items[args.name] = args.path
                else:
                    raise Exception('ERROR: please supply a path name to the data you wish to load. See the the help for details')
            
            content = ['%s:%s'% (key, value) for key, value in items.iteritems()]

        if path:
            if not os.path.exists(path):
                raise Exception('ERROR: path (%s) doesn\'t exist' % (path))
        else:
            path = args.path

        if content:
            utils.write_to_file(path_to_file, '\n'.join(content), mode='w')

        print 'Loading data from %s' % (path)

        
        # from hip import setup
        # setup.install(path)

        os.system('%s %s packages -o install -s %s"' % (path_to_virtual_env, os.path.normpath(os.path.join(here, '..', 'manage.py')), path))
    
    except Exception as e:
        print str(e)
        print 'Available aliases:'
        print content or 'None'
        sys.exit(1)

parser_start = subparsers.add_parser(
    'load',
    help="load data into the application",
)
parser_start.add_argument(
    '-p', '--path',
    help="path to the 'source_data' directory, defaults to %s" % (os.path.join(here, 'source_data')),
    type=str, 
    #default=(os.path.join(here, 'source_data')),
)
parser_start.add_argument(
    '-n', '--name',
    help="Name to alias the path to the package",
    type=str,
)
COMMANDS['load'] = command_load


def command_help(args):
    argv = ['--help']
    if args.task:
        argv.append(args.task)
    return parser.parse_args(argv[::-1])

parser_help = subparsers.add_parser(
    'help',
    help="describe available commands or one specific command",
)
parser_help.add_argument('task', help='task to show help for', nargs='?')
COMMANDS['help'] = command_help


def main(argv=None):
    if argv is not None:
        args = parser.parse_args(argv)
    else:
        args = parser.parse_args()

    try:
        COMMANDS[args.command](args)
    except CommandError as e:
        log.error(str(e))
        sys.exit(1)


if __name__ == '__main__':
    main()