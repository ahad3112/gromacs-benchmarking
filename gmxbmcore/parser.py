'''
    Author:
        * Muhammed Ahad <ahad3112@yahoo.com, maaahad@gmail.com, maaahad@kth.se>
    Desctiption:
        This module collect data from the GROMACS output file
'''

# Python stdlib
import os
import hashlib
import json
# reframe
import reframe as rfm
import reframe.utility.sanity as sn

# in house
from utilities import utility

def extract_info_as_dict(obj, patterns, sanity_func=sn.extractsingle):
    if obj.stagedir and os.path.exists(obj.stagedir):
        file = os.path.join(obj.stagedir, obj.output_file)
        if os.path.exists(file):
            info = {}
            for pattern in patterns:
                info[pattern] = sanity_func(
                    patterns[pattern],
                    file,
                    pattern,
                    str
                ).evaluate()

            return info

    raise RuntimeError('Simulation generated output file not found.')


def cpu_info(obj):
    '''
         Brand:  Intel(R) Xeon(R) CPU E5-2690 v3 @ 2.60GHz
    '''
    patterns = {
        'brand': r'\s*Brand:\s*(?P<brand>.*)',
    }
    return extract_info_as_dict(obj, patterns)


def gpu_info(obj):
    patterns = {
        'card': r'\s*#[0-9]+:\s*(?P<card>.*)'
    }
    return extract_info_as_dict(obj, patterns, sanity_func=sn.extractall)


def machine_info(obj):
    info = {'cpu': cpu_info(obj)}
    if obj.gpu_enabled:
        info.update({'gpu': gpu_info(obj)})

    return info


def gromacs_info(obj):
    '''
    GROMACS version:    2020.1
    Precision:          single
    SIMD instructions:  AVX2_256
    '''
    patterns = {
        'version': r'GROMACS version:[ \t]+(?P<version>[0-9]{4}\.[0-9]{1})',
        'precision': r'Precision:[ \t]+(?P<precision>.*)',
        'simd': r'SIMD instructions:[ \t]+(?P<simd>.*)',
    }
    return extract_info_as_dict(obj, patterns)


def binaries_info(obj):
    info = {
        'gmx': gromacs_info(obj),
        # other binaries : will be added as required
    }

    # update  gmx in info with the binary hash
    # signature : utility.hash(*,bytes_string_list=[],alg='sha1', length=None)
    bin_lib_hash = utility.hash(bytes_string_list=[open(obj.gmx_binary, 'rb').read(),
                                                   open(obj.libgromacs, 'rb').read()],
                                alg='md5',
                                length=10)

    info.get('gmx', {}).update({'bin_lib_hash': bin_lib_hash})

    return info


def libraries_info(obj):
    '''
    FFT library:        fftw-3.3.7-sse2-avx-avx2-avx2_128-avx512
    MPI library:        MPI
    '''
    patterns = {
        'FFTW': r'FFT library:[ \t]+(?P<FFTW>.*)',
        'MPI': r'MPI library:[ \t]+(?P<MPI>.*)'
    }

    return extract_info_as_dict(obj, patterns)


# TODO : add a function to extract compiler info
def c_compiler(obj):
    patterns = {
        'version': '\s*C compiler:\s*.*?\s(?P<version>.*)',
        'flags': '\s*C compiler flags:\s*(?P<flags>.*)'
    }

    return extract_info_as_dict(obj, patterns)

def cpp_compiler(obj):
    patterns = {
        'version': '\s*C\+\+ compiler:\s*.*?\s(?P<version>.*)',
        'flags': '\s*C\+\+ compiler flags:\s*(?P<flags>.*)'
    }

    return extract_info_as_dict(obj, patterns)

def cuda_compiler(obj):
    patterns = {
        'version': '\s*CUDA compiler:\s*.*?\s(?P<version>release .*)',
        'flags': '\s*CUDA compiler flags:\s*(?P<flags>.*)',
        'driver': '\s*CUDA driver:\s*(?P<driver>.*)',
        'runtime': '\s*CUDA runtime:\s*(?P<runtime>.*)',
    }

    return extract_info_as_dict(obj, patterns)

def compilers_info(obj):
    info = {
        'C': c_compiler(obj),
        'C++': cpp_compiler(obj),
    }

    if obj.gpu_enabled:
        info.update({'CUDA': cuda_compiler(obj)})

    return info


def gmx_log_info(obj):
    patterns = {
        'steps_override': '(?P<steps_override>Overriding nsteps with value passed on the command line:\s*.*)',
        'nstlist': '(?P<nstlist>Changing nstlist from .*)',
        'bonded_kernel': '(?P<bonded_kernel>Using .*? nonbonded .*? kernels)',
        'pme_grid': '(?P<pme_grid>.*? pme grid .*)',
        'update_groups': '\s*Using update groups, (?P<update_groups>.*)',
    }

    info = extract_info_as_dict(obj, patterns, sanity_func=sn.extractall)
    return {key:list(set(value)) for (key, value) in info.items()}

def simulation_input_info(obj):
    '''
        integrator                     = md
        dt                             = 0.002
        nsteps                         = 200000
    '''
    patterns = {
        'integrator': '\s*integrator\s*=\s*(?P<integrator>.*)',
        'dt': '\s*dt\s*=\s*(?P<dt>.*)',
        'nsteps': '\s*nsteps\s*=\s*(?P<nsteps>.*)',

    }

    return extract_info_as_dict(obj, patterns)
