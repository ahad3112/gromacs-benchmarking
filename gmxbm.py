#!/usr/bin/env python
'''
Author:
    * Muhammed Ahad <ahad3112@yahoo.com, maaahad@gmail.com, maaahad@kth.se>
Usage:
    $ ./gmxbm.py -h
Description
    *
'''
import os
import sys
import argparse

from gmxbmcore.cli.run import add_run_cli



if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=r'Automatize benchmark tool for "GROMACS"',
        add_help=True
    )

    sub_parsers = parser.add_subparsers(
        title='list of sub-modules',
        description=('Submodules are responsible for generating '
                     'prepare,run, analyze scripts for the regression tests.'),
    )


    # adding parsers to the subparsers
    add_run_cli(sub_parsers)


    args = parser.parse_args()


    try:
        args.handler(args)
    except AttributeError:
        raise RuntimeError(f'No Command handler handler found... for {args}')
