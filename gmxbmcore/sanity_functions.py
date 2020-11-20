'''
    Author:
        * Muhammed Ahad <ahad3112@yahoo.com, maaahad@gmail.com, maaahad@kth.se>
    Desctiption:
        This module contains sanity_functions related to GROMACS
        * Sanity Checking : Finished mdrun ,
        * Gromacs Info : version, precision, simd
        * Hardware info : cpu info, gpu info
        * Simulation input info : Not Decided Yet...
        * Performace variables : sn/day, hr/ns
'''


# Python stdlib
import os
import json
# reframe
import reframe as rfm
import reframe.utility.sanity as sn

# in house


@sn.sanity_function
def ns_per_day(obj):
    nspd = sn.extractsingle(
        r'^Performance:\s+(?P<nspd>\S+)\s+.*',
        obj.output_file,
        'nspd',
        float
    )

    return nspd


@sn.sanity_function
def hr_per_ns(obj):
    hrpns = sn.extractsingle(
        r'^Performance:\s+\S+\s+(?P<hrpns>\S+)$',
        obj.output_file,
        'hrpns',
        float
    )

    return hrpns
