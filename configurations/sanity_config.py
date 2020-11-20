'''
    Author:
        * Muhammed Ahad <ahad3112@yahoo.com, maaahad@gmail.com, maaahad@kth.se>
    Desctiption:
        This is the place where the developer will configure their sanity patterns
        for consistancy checking
'''
# python standard library

# reframe

# in-house

assert_found = (
    r'Finished mdrun',
)

assert_reference = dict(
    # energy={
    #     'pattern': (r'\s+Potential\s+Kinetic En\.\s+Total Energy'
    #                 r'\s+Conserved En\.\s+Temperature\n'
    #                 r'(\s+\S+){2}\s+(?P<energy>\S+)(\s+\S+){2}\n'
    #                 r'\s+Pressure \(bar\)\s+Constr\. rmsd',),
    #     'ref_value': -3270799.9,
    #     'lower_thres': None,
    #     'upper_thres': None
    # },
    walltime={
        'pattern': (r'\s*Time:\s*\d*\.\d*\s*(?P<walltime>\d*\.\d*)\s*\d*\.\d*'),
        'ref_value': 30.0,
        'lower_thres': 0.0,
        'upper_thres': None
    }
)
