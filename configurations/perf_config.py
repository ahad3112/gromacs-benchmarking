'''
    Author:
        * Muhammed Ahad <ahad3112@yahoo.com, maaahad@gmail.com, maaahad@kth.se>
    Desctiption:
        This is the place where the developer will configure their performance
        variables along with the reference values
'''
# python standard library

# reframe

# in-house
from gmxbmcore import sanity_functions as gmx_sanity_functions

perf_patterns = {
    'ns/day': gmx_sanity_functions.ns_per_day,
    # 'hr/ns': gmx_sanity_functions.hr_per_ns,
}

reference = {
    'Tegner': {
        'ns/day': (None, None, None, None),
        # 'hr/ns': (None, None, None, None),
    },
    'Beskow': {
        'ns/day': (None, None, None, None),
        # 'hr/ns': (None, None, None, None),
    },
}
