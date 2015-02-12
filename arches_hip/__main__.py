import argparse
import codecs
import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "arches_hip.settings")
here = os.path.abspath(os.path.dirname(__file__))
COMMANDS = {}

def get_arches_env():
    with codecs.open(os.path.normpath(os.path.join(here, '..', 'Procfile')), 'r', encoding='utf-8-sig') as f: 
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
    prog='arches_hip', 
    description='Manage Arches-based Applications',
    parents=[parent_parser], 
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

subparsers = parser.add_subparsers(title='available commands', dest='command')
subparsers.required = True


def command_run_es(args):
    os.system('%s %s packages -o start_elasticsearch' % (path_to_virtual_env, os.path.normpath(os.path.join(here, '..', 'manage.py'))))

parser_start = subparsers.add_parser(
    'runsearchengine',
    help="Starts the elasticsearch process",
)
COMMANDS['runsearchengine'] = command_run_es


def command_runserver(args):
    os.system('%s %s runserver %s' % (path_to_virtual_env, os.path.normpath(os.path.join(here, '..', 'manage.py')), args.port))

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
    os.system('%s %s packages -o install' % (path_to_virtual_env, os.path.normpath(os.path.join(here, '..', 'manage.py'))))

parser_start = subparsers.add_parser(
    'load',
    help="load data into the application",
)
COMMANDS['load'] = command_load


def command_resource_load(args):
    if args.source != '':
        os.system('%s %s packages -o load_resources --source "%s"' % (path_to_virtual_env, os.path.normpath(os.path.join(here, '..', 'manage.py')), args.source))
    else:
        os.system('%s %s packages -o load_resources' % (path_to_virtual_env, os.path.normpath(os.path.join(here, '..', 'manage.py'))))


parser_start = subparsers.add_parser(
    'load_resources',
    help="load resource data into the application",
)
parser_start.add_argument(
    '-s', '--source',
    help="external data source - arches or shapefile",
    type=str, 
    default='',
)
COMMANDS['load_resources'] = command_resource_load


def command_remove_resources(args):
    os.system('%s %s packages -o remove_resources -l %s' % (path_to_virtual_env, os.path.normpath(os.path.join(here, '..', 'manage.py')), args.load_id))

parser_start = subparsers.add_parser(
    'remove_resources',
    help="remove resource data from a previous load given a loadid",
)
parser_start.add_argument(
    '-l', '--load_id',
    help="identifier for a particular resource load",
    type=str, 
    default='',
)
COMMANDS['remove_resources'] = command_remove_resources


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