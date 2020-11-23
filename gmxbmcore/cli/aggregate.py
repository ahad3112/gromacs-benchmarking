'''
    Author:
        * Muhammed Ahad <ahad3112@yahoo.com, maaahad@gmail.com, maaahad@kth.se>
    Desctiption:
        -------------
'''
import os

# in-house
from gmxbmcore.handlers.aggregate import handler

def valid_path(path):
    if not os.path.isabs(path):
        return os.path.join(os.getcwd(), path)

    return path

def exist_or_create(path):
    v_path = valid_path(path)
    if not os.path.exists(v_path):
        os.system('mkdir -p {0}'.format(v_path))

    return v_path


def add_aggregate_cli(sub_parsers):
    aggregate_parser = sub_parsers.add_parser(
        'aggregate',
        help=r'Aggregate benchmark result',
        description=(r'This module combined two or more benckmak results directories '
                     'into a single directory tree.')
    )

    aggregate_parser.set_defaults(handler=handler)
    aggregate_parser.add_argument('-i', '--inputs',type=valid_path, nargs='+',
                                  help=('Space separated list of input directory. '
                                         'If abs path is not provided, path will '
                                         'be resolved relative to the current '
                                         'working directory.'))

    aggregate_parser.add_argument('-o', '--output',type=exist_or_create, required=True,
                                  help=('Output directory for the combined '
                                         'result. If abs path is not provided, '
                                         'path will be resolved relative to '
                                         'current working directory.'))
