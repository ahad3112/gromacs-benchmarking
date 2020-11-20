'''
    Author:
        * Muhammed Ahad <ahad3112@yahoo.com, maaahad@gmail.com, maaahad@kth.se>
    Desctiption:
        -------------
'''
# Python stdlib
import sys
import os
import glob
import subprocess
import shelve
import json
import time
import uuid
import re

# we need to append the directory to the gmxbm.py which is available via
# environment variable GMXBM_PATH
sys.path.append(os.getenv('GMXBM_PATH', ''))
# in-house
from gmxbmcore import sanity_functions as gmx_sanity_functions
from configurations import perf_config, sanity_config
from gmxbmcore import parser as gmx_parser
from gmxbmcore.reports import GMXPerformanceReport
from utilities.formatter import format_performance_dict
from utilities import utility

# reading the user provided args
# We are in the output directory and the args in in the output dir
# However we may use the absolute path
s = shelve.open('args')
args = s.get('args', None)
s.close()
if not args:
    raise RuntimeError('Implementation Error : User args are missing!')



# reframe
import reframe as rfm
import reframe.utility.sanity as sn


@rfm.simple_test
class GromacsRegressionTest(rfm.RunOnlyRegressionTest):
    def __init__(self):
        self.descr = args.descr
        self.valid_systems = args.machines
        self.valid_prog_environs = args.prog_envs

        self.gpu_enabled = True if args.gpu else False

        # need to choose between gmx amd gmx_mpi
        if args.gmx:
            self.executable = args.gmx
        else:
            self.executable = 'gmx_mpi' if args.mpi else 'gmx'

        # self.executable will be overriden by reframe, so we need to keep
        # record of executable to be used in generating binary hash
        self.gmx_binary_name = self.executable

        # output file name
        self.gmx_output_prefix = 'gmx_md'
        self.output_file = self.gmx_output_prefix + '.log'

        input_path = args.input

        self.executable_opts = ['mdrun', '-s', input_path, '-deffnm', self.gmx_output_prefix]

        # adding OMP threads
        if args.ntomp:
            self.executable_opts.append(f'-ntomp $OMP_NUM_THREADS')

        # resoureces for this test
        # if mpi was not enabled, RuntimeError already been raised during args_checks
        self.time_limit = args.wall_time
        self.num_tasks = args.nprocs
        self.num_tasks_per_node = args.nprocs // args.nnodes

        # environment variables
        for env in args.envs:
            name, value = GromacsRegressionTest.extract_env(env)
            if name in self.variables:
                self.variables[name] += f':{value}'
            else:
                self.variables[name] = value

        # exporting OMP_NUM_THREADS
        if args.ntomp:
            self.variables['OMP_NUM_THREADS'] = args.ntomp

        self.perf_patterns = {k:v(self) for (k,v) in perf_config.perf_patterns.items()}

        # maintainers and tags
        self.maintainers = args.maintainers

    @staticmethod
    def extract_env(env):
        env = env.split(':')
        if args.prepend_env:
            return (env[0].strip(), env[1].strip() + ':$' + env[0].strip())
        else:
            return (env[0].strip(), '$' + env[0].strip() + ':' + env[1].strip())


    def get_uid(self):
        milliseconds = int(round(time.time() * 1000))
        return utility.hash(
            bytes_string_list=[milliseconds.to_bytes(6, 'little')],
            alg='md5',
            length=10
        )

    def set_id(self):
        '''
        This method generate unique ID for the test. perflogs, gmx-outputs and
        reports will use this ID.
        '''
        self.id = '{bin_lib_hash}_{id}'.format(
            bin_lib_hash=self.gromacs_info['bin_lib_hash'],
            id=self.get_uid()
        )


    def set_storage(self):
        gmx_storage = os.path.join(args.outputdir,
                                   (f'gmx-outputs/{self.gromacs_info["version"]}/'
                                    f'{self.current_system.name}/'
                                    f'{self.current_partition.name}'))

        if not os.path.exists(gmx_storage):
            os.system(f'mkdir -p {gmx_storage}')

        self.storage = os.path.join(gmx_storage, f'{self.id}')

    @rfm.run_after('setup')
    def set_gmx_bin_lib_path(self):
        # we need to temporality prepend the config.py path to sys.path
        # once job is done, we remove the path
        config_path, config_file = os.path.split(args.config_file)
        config_file = os.path.splitext(config_file)[0]
        sys.path.insert(0, config_path)
        config = __import__(config_file)

        try:
            site_configuration = getattr(config,'site_configuration')
        except:
            raise RuntimeError(f'${args.config_file} must contains site_configuration attribute.')

        # getting the list of modules for the current environment
        module_list = []
        for env in site_configuration.get('environments', []):
            if env.get('name', '') == self.current_environ.name:
                module_list = env.get('modules', [])

        # taking all value of PATH from module
        bin_path_from_modules = []
        lib_path_from_modules = []
        for module in module_list:
            temp_file = os.path.join(os.getcwd(), 'temp')
            bin_path_pattern = '.*?\s+PATH\s+(.*)'
            lib_path_pattern = '.*?\s+LD_LIBRARY_PATH\s+(.*)'
            os.system(r'module show {0} &> {1}'.format(module, temp_file))

            module_content = open(temp_file, 'r').read()
            bin_path_from_modules.extend(
                re.findall(bin_path_pattern, module_content)
            )
            lib_path_from_modules.extend(
                re.findall(lib_path_pattern, module_content)
            )
            os.system(r'rm {0}'.format(temp_file))

        # User provided PATH will be given priority
        PATH = self.variables.get('PATH','') + ':' + ':'.join(bin_path_from_modules)
        self.gmx_binary = None
        for path in PATH.split(':'):
            path = path.strip()
            if path and not path.startswith('$'):
                bin_path = os.path.join(path, self.gmx_binary_name)
                if os.path.exists(bin_path):
                    self.gmx_binary = bin_path
                    break

        if not self.gmx_binary:
            raise RuntimeError('GMX binary path was not provided or not found.')

        # User provided LD_LIBRARY_PATH will be given priority
        self.libgromacs = None
        LD_LIBRARY_PATH = self.variables.get('LD_LIBRARY_PATH','') + ':' + \
        ':'.join(lib_path_from_modules)

        for ld_lib_path in LD_LIBRARY_PATH.split(':'):
            ld_lib_path = ld_lib_path.strip()
            if ld_lib_path and not ld_lib_path.startswith('$'):
                lib_path = os.path.join(
                    ld_lib_path,
                    'libgromacs{0}.a'.format(self.gmx_binary_name[3:])
                )
                if os.path.exists(lib_path):
                    self.libgromacs = lib_path
                    break

        if not self.libgromacs:
            raise RuntimeError(('GMX library path was not provided or not found. '
                                'Please provide LD_LIBRARY_PATH using --envs option.'))

        # removing config path from sys.path
        del sys.path[0]



    @rfm.run_after('setup')
    def add_sanity(self):
        assert_references = []
        for (perf_v, props) in sanity_config.assert_reference.items():
            assert_references.append(
                sn.assert_reference(
                    sn.extractsingle(props['pattern'],
                                     self.output_file,
                                     perf_v, float,
                                     item=-1),
                    props['ref_value'],
                    props['lower_thres'],
                    props['upper_thres']
                )
            )

        self.sanity_patterns = sn.all([
            *[sn.assert_found(af, self.output_file) for af in sanity_config.assert_found],
            *assert_references
        ])


    @rfm.run_after('setup')
    def add_performance_reference(self):
        self.reference = {
            self.current_system.name: perf_config.reference.get(self.current_system.name, {})
        }


    @rfm.run_before('performance')
    def extract_info(self):
        '''
        This method extract information regarding the test. The extracted info
        will be used in generating performance report for the test.
        '''
        self.binaries_info = gmx_parser.binaries_info(self)
        self.gromacs_info = self.binaries_info.get('gmx', 'Not Available')
        self.compilers_info = gmx_parser.compilers_info(self)
        self.machine_info = gmx_parser.machine_info(self)
        self.sim_input_info = gmx_parser.simulation_input_info(self)
        self.libraries_info = gmx_parser.libraries_info(self)
        self.gmx_log_info = gmx_parser.gmx_log_info(self)

        # setting the identifiers for the test
        self.set_id()

        # Setting up test storage path for storing gmx output.. assumes
        # self.id is already generated
        self.set_storage()

        # self.tags will be used to add addition information to the log report
        self.tags = {
            (
                f'id={self.id}'
            )
        }

    @rfm.run_before('cleanup')
    def extract_performance_info(self):
        '''
        As we don't have option to get access to what will be in the ReFrame
        generated performance report, so we have to re-create the performance
        info here to be stored along other info in the machine readable report
        file.
        '''
        # we need the absolute path to the test output as we are getting performance variable on the
        # non-default way
        self.output_file = os.path.join(self.stagedir, self.output_file)

        self.performance_info = {key:value.evaluate() for (key, value) in self.perf_patterns.items()}

        # self.reference is of type reframe.utility.ScopedDict.
        # So we need to follow the iteration protocol implemented by reframe.utility.ScopedDict
        for key, value in self.reference.items():
            system, perf_var = key.split(':')
            if system == self.current_system.name:
                unit = value[3] or '(no unit specified)'
                if self.performance_info.get(perf_var, None):
                    self.performance_info[perf_var] = f'{self.performance_info[perf_var]} {unit}'

        # adding num_tasks to the performance info
        self.performance_info['num_tasks'] = self.num_tasks

    @rfm.run_before('cleanup')
    def report(self):
        '''
        This method is reponsible to generate a machine readable performace report file,
        The name of the file will be the uid of the test
        '''
        GMXPerformanceReport(test=self, outputdir=args.outputdir).dump()

    @rfm.run_before('cleanup')
    def store_gmx_output(self):
        '''
        This method is responsible to copy GROMACS generated output files to a
        folder named after the uid of the test and the folder will be stored in
        a predefined directory in the working directory.
        '''
        os.system(f'mkdir {self.storage}')

        os.system('cp -r {0} {1}/'.format(
            os.path.join(self.stagedir, f'{self.gmx_output_prefix}*'),
            self.storage
        ))
