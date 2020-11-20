'''
    Author:
        * Muhammed Ahad <ahad3112@yahoo.com, maaahad@gmail.com, maaahad@kth.se>
    Desctiption:
        This module will implement some utility routines
'''
# python stdlib
import hashlib


def hash(*,bytes_string_list=[],alg='md5', length=None):
    routine = getattr(hashlib, alg)
    if routine:
        m = routine()
        for string in bytes_string_list:
            m.update(string)

        hex_digest = m.hexdigest()

        if length:
            return hex_digest[:length]

        return hex_digest
    else:
        raise RuntimeError(
            f'{alg} : Wrong hash algorithm chosen. '
            f'Available algorithms are: \n{hashlib.algorithms_available}'
        )
