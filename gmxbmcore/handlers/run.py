'''
    Author:
        * Muhammed Ahad <ahad3112@yahoo.com, maaahad@gmail.com, maaahad@kth.se>
    Description:
        This Subcommand is responsible to utilize the user's input to generate appropriate Gromacs test case

'''

import os
import sys
import argparse
import shelve
import glob
import subprocess
import re


# path to reframe, site configuration, test class and log files
# ReFrame path will be resolved against ReFrame installation path

def check_args(args):
    if args.nnodes is not None:
        if args.nprocs is None:
            raise RuntimeError('--nprocs is required in case --nnodes is provided')
        else:
            if args.nprocs % args.nnodes != 0:
                raise RuntimeError('--nprocs should be multiple of --nnodes')

    if args.nprocs > 1 and not args.mpi:
        raise RuntimeError(r'mpi should be enabled (--mpi) if --nprocs > 1')


def clear_args(args_path):
    args_files = glob.glob(os.path.join(args_path,'args.*'))
    for args_file in args_files:
        os.system(f'rm {args_file}')

def handler(args):
    # checking whether the arguments was provided as expected
    check_args(args)

    # setting output directory as current working directory
    os.chdir(args.outputdir)


    # Test Path is fixed within apps/gromacs/ . Home directory as the user might run
    # benchmark script from another directory other than the directory to gmxbm source
    test_path = os.path.join(os.path.abspath(sys.path[0]),
                             'apps/gromacs/test.py')

    # output logs
    logs_directory_path = os.path.join(args.outputdir, 'logs')
    reframe_stdout_path = os.path.join(logs_directory_path, 'reframe.out')

    reframe_kill_path = os.path.join(logs_directory_path, 'kill-reframe.sh')

    # arg path will be the current working directory i.e. output directory
    args_path = os.getcwd()

    # removing all contents from the logs directory if exists,
    # create the directory otherwise
    if os.path.exists(logs_directory_path):
        if os.path.isdir(logs_directory_path):
            os.system(f'rm -rf {logs_directory_path}/*')
        else:
            f'rm {logs_directory_path}'
    else:
        os.system(f'mkdir {logs_directory_path}')

    # we spawns a child process that is reponsible to run reframe internally
    pid = os.fork()
    if pid == 0:
        clear_args(args_path)
        # storing user provided args to be used during Test class creation
        # This will be stored in cwd, i.e. output directory provided by user
        # default directory is current working directory
        s = shelve.open(os.path.join(args_path,'args'))
        s['args'] = args
        s.close()

        # setting path to gmxbm.py, as in Test class creation we need to append
        # this path to Python module search path to make all scripts in gmxbm available
        os.environ['GMXBM_PATH'] = os.path.abspath(sys.path[0])

        # running reframe using installed reframe
        command = f'reframe -C {args.config_file} -c {test_path} -r'

        pipe = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)

        # this will create a executable script to kill Reframe that is running
        # in background
        with open(reframe_kill_path, 'w') as file:
            file.write(f'#!/bin/bash\nkill -15 {str(pipe.pid)}')

        os.system(f'chmod +x {reframe_kill_path}')

        # standard output from ReFrame
        with open(reframe_stdout_path, 'w') as file:
            file.write(pipe.communicate()[0].decode())

        # cleaning process starts here for our module
        clear_args(args_path)

        # removing kill-reframe.sh
        os.system(f'rm {reframe_kill_path}')

        # moving reframe log files, performance log file to that logs directory
        os.system(f'mv {os.path.join(os.getcwd(), "*.log")} {logs_directory_path}')

        os._exit(0)
    else:
        print((f'\nkill-reframe.sh, reframe.log and reframe.out(after reframe '
               f'finishes) available at {logs_directory_path}\n'))
