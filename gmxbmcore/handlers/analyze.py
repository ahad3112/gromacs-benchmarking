'''
    Author:
        * Muhammed Ahad <ahad3112@yahoo.com, maaahad@gmail.com, maaahad@kth.se>
    Description:
        This is the hander module for the analyze sub-command

'''
# python stdlib
import os
import glob
import json

# in-house
from utilities.formatter import format_performance_dict

__reports_dir = os.path.join(os.getcwd(), 'reports')

def report(*, args, test_seq):
    for test in test_seq:
        test_path = os.path.join(__reports_dir , test)
        if not os.path.exists(test_path):
            raise RuntimeError(f'No test in record with id : {test}')

        test_report = json.load(open(test_path))

        print(format_performance_dict(test_report, indent=4, start='Formatted Test Report : \n'))


def handler(args):
    if not os.path.exists(__reports_dir):
        raise RuntimeError(f'No reports/ directory exists in {os.getcwd()}')

    if args.id:
        if args.report:
            report(args=args, test_seq=[args.id + '.json'])
