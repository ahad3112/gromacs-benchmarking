'''
    Author:
        * Muhammed Ahad <ahad3112@yahoo.com, maaahad@gmail.com, maaahad@kth.se>
    Desctiption:
        This is the analyze module and will be used for:
            * generating report for specified test, ...
            * ---
'''
# python stdlib
import argparse

# in-house
from gmxbmcore.handlers.analyze import handler


def add_analyze_cli(sub_parsers):
    analyze_parser = sub_parsers.add_parser(
        'analyze',
        help='This module will be used to analyze the stored performance report.',
        description=(
            'This module should be able to generate more human-friendly '
            'performance report based on the user provided test id, '
            'plot performance result, and ...'
        )
    )

    # handler
    analyze_parser.set_defaults(handler=handler)

    # adding argument
    # Test related group
    test_group = analyze_parser.add_mutually_exclusive_group(required=True)
    test_group.add_argument(
        '--id',
        type=str,
        help='ID of the test to be analyzed',
    )
    test_group.add_argument(
        '--gmx',
        type=str,
        help=('(NOT IMPLEMENTED YET) '
              'All the tests for this GROMACS version will be used in analysis.'),
    )

    # report related group
    report_group = analyze_parser.add_mutually_exclusive_group(required=True)
    report_group.add_argument(
        '--report',
        action="store_true",
        help='Generate human friendly report.'
    )

    # report_group.add_argument(
    #     '--plot',
    #     action="store_true",
    #     help='Plot the performance result....DONT KNOW YET HOW SHOULD WE DO THIS'
    # )
