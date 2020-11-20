'''
    Author:
        * Muhammed Ahad <ahad3112@yahoo.com, maaahad@gmail.com, maaahad@kth.se>
    Desctiption:
        This module format output text as necessary
'''


def format_performance_dict(pdict, indent=0, start=''):
    result = start
    line_format = '{0}- {1:<}: {2:<}\n'
    for key in pdict:
        if isinstance(pdict[key], dict):
            result += line_format.format(' ' * indent, key, '') + format_performance_dict(pdict[key], indent + 3)
        else:
            result += line_format.format(' ' * indent, key, pdict[key])

    return result
