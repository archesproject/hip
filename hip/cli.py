import argparse
import codecs
import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hip.settings")

from hip import setup
from hip import version
from arches.management.commands import utils

here = os.path.abspath(os.path.dirname(__file__))
COMMANDS = {}

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
parent_parser.add_argument(
    '-v', '--version',
    action='version', version='%(prog)s' + ' Version %s : Build %s' % (version.__VERSION__, version.__BUILD__))

parser = argparse.ArgumentParser(
    prog='hip', 
    description='Manage Arches-based Applications',
    parents=[parent_parser], 
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

subparsers = parser.add_subparsers(title='available commands', dest='command')
subparsers.required = True


def command_load(args):
    filename = 'data_paths.txt'
    path = None
    if args.name:
        try:
            with codecs.open(os.path.join(here, filename), 'r', encoding='utf-8-sig') as f: 
                for row in f:
                    if row.split(':')[0] == args.name:
                        path = ':'.join(row.split(':')[1:]).strip()
                        break
        except:
            utils.write_to_file(os.path.join(here, filename), '%s: %s' % (args.name, args.path), mode='a')
    
    if path:
        if not os.path.exists(path):
            print 'ERROR: path (%s) aliased to the name "%s" doesn\'t exist' % (path, args.name)
            sys.exit(1)
    else:
        path = args.path
            
    print 'Loading data from %s' % (path)
    setup.install(path)

parser_start = subparsers.add_parser(
    'load',
    help="load data into the application",
)
parser_start.add_argument(
    '-p', '--path',
    help="path to the 'source_data' directory, defaults to %s" % (os.path.join(here, 'source_data')),
    type=str, 
    default=(os.path.join(here, 'source_data')),
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