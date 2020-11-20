'''
    Author:
        * Muhammed Ahad <ahad3112@yahoo.com, maaahad@gmail.com, maaahad@kth.se>
    Desctiption:
        -------------
'''
import os
import sys
import argparse
import shelve
import glob
import subprocess
import re


from gmxbmcore.handlers.run import handler


__site_configuration_path = os.path.join(os.path.abspath(sys.path[0]),
                                         'configurations/config.py')



def valid_env(env):
    if ':' in env:
        if len(env.split(':')) != 2:
            raise argparse.ArgumentTypeError(f'{env} is not confronted with name:value format.')
    else:
        raise argparse.ArgumentTypeError(f'{env} is not confronted with name:value format.')

    return env


def valid_walltime(wall_time):
    # <days>d<hours>h<minutes>m<seconds>s
    pattern = '^([0-9]+d)?([0-9]+h)?([0-9]+m)?([0-9]+s)?$'
    if not re.match(pattern, wall_time):
        raise argparse.ArgumentTypeError((f'{wall_time} is not confronted with '
                                          '<days>d<hours>h<minutes>m<seconds>s format.'))

    return wall_time


def valid_path(path):
    if not os.path.isabs(path):
        return os.path.join(os.getcwd(), path)

    return path

def exist_or_create(path):
    v_path = valid_path(path)
    if not os.path.exists(v_path):
        os.system('mkdir -p {0}'.format(v_path))

    return v_path

def exist_or_raise_error(path):
    v_path = valid_path(path)
    if not os.path.exists(v_path):
        raise RuntimeError('{0} does not exists.'.format(v_path))

    return v_path

def add_run_cli(sub_parsers):
    run_parser = sub_parsers.add_parser(
        'run',
        help=r'This module initiate the regression test pipelines of "ReFrame"',
        description=(r'Generate Regression test/tests based on users provided '
                     'input and initiate ReFrame\'s regression test pipeline.')
    )

    # handler
    run_parser.set_defaults(handler=handler)

    # mandatory arguments
    run_parser.add_argument('-i', '--input', type=exist_or_raise_error, required=True,
                            help=('input (.tpr) file Use ("REQUIRED"). In case '
                                  'absolute path is not given, the path will be '
                                  'resolved against current working directory.')
                            )
    # configuration file : optinal
    run_parser.add_argument('-C', '--config-file', type=str,
                            help=('Machine confguration file. In case absolute path '
                                  'is not given, the path will be resolved against '
                                  'current working directory.'
                                  f'( EDITABLE default: {__site_configuration_path}).'
                                  ),
                            default=__site_configuration_path)
    # optional arguments
    run_parser.add_argument('--machines', type=str, nargs='*',
                            metavar="cluster:partition",
                            help=('Machines list where to run benchmark tests. '
                                  f'(default: {["*"]}), this includes all clusters'
                                  ' and partitions combination in the machie config file.'),
                            default=['*'])

    run_parser.add_argument('--prog-envs', type=str, nargs='*',
                            help=('Space separated list of valid programming '
                            f'environments. (default{["*"]}), this includes all'
                            ' available programming environments in the machine '
                            'config file.'),
                            default=['*'])
    run_parser.add_argument('--nnodes', type=int,
                            help=(f'Total Number of "nodes" to be used for '
                                  f'benchmark test/tests. (default : {1}).'),
                            default=1)
    run_parser.add_argument('--nprocs', type=int,
                            help=(f'Total Number of "processors" (multiple of --nnodes)'
                                  f' to be used for benchmark test/tests. (default : {1}).'),
                            default=1)
    run_parser.add_argument('--ntomp', type=str, help=r'Number of OMP "thread".')
    run_parser.add_argument('--gpu', action='store_true',
                            help=('This will enable reporting GPU related info, '
                                  'in case the partition you chose uses any '
                                  'GPU resources.'))
    run_parser.add_argument('--mpi', action='store_true',
                            help=(r'Enable "MPI". If enabled, make sure that '
                                  r'chosen machine/machines (cluster:partition) '
                                  r'have parallel launcher such mpirun or srun.'))

    run_parser.add_argument('--envs', type=valid_env, nargs='*', metavar='name:value',
                            help=(r'List of environment variables: default is empty list. '
                                  r'"value" will be appended to the variable "name" '
                                  r'unless --prepend-env argument is specified.'),
                            default=[])

    run_parser.add_argument('--prepend-env', action='store_true',
                            help=('if specified values provided by "--envs" '
                                  'argumentwill be prepended to the corresponding '
                                  'env variable.'))

    run_parser.add_argument('--outputdir', type=exist_or_create,
                            help='Path to output directory. In case absolute path '
                                  'is not given, the path will be resolved against '
                                  f'current working directory. (default {os.getcwd()})',
                            default=os.getcwd())

    run_parser.add_argument('--wall-time',
                            type=valid_walltime,
                            metavar='<days>d<hours>h<minutes>m<seconds>s',
                            help=('Time limit for the benchmark test/tests. This '
                                  'is required in case the user would like to run '
                                  'benchmark tests to the queue system in cluster. '
                                  '(default : 10m). Example : 2h30m.'),
                            default='10m')


    run_parser.add_argument('--gmx', type=str, required=True,
                            help=('Name of the GMX binary. Make sure to specify '
                                  'PATH to GMX binary using the --envs option, '
                                  'in case the machine partirion does not have '
                                  'gromacs module to be loaded explicitly.'))


    # The following are optional and not important options
    run_parser.add_argument('--descr', type=str,
                            help='description of the test',
                            default='GROMACS Benchmark/Regression Test')
    run_parser.add_argument('--maintainers',
                            type=str,
                            nargs='*',
                            help=r'Test maintainers: default (output of "whoami")',
                            default=[os.popen('whoami').read().strip()])
