'''
Machine Configuration file
'''
site_configuration = {
    'systems': [
        {
            'name': 'Beskow',
            'descr': 'Beskow at PDC',
            'hostnames': ['\s*\.*?beskow.*'],
            'modules_system': 'tmod4',
            'partitions': [
                {
                    'name': 'interactive_module',
                    'scheduler': 'local',
                    'launcher': 'srun',
                    'environs': ['gromacs_2020_4'],
                },
                {
                    'name': 'queue',
                    'scheduler': 'slurm',
                    'launcher': 'srun',
                    'access': ['-A pdc.staff'],
                    'environs': ['gromacs_2020_4'],
                },
            ],
        },
        {
            'name': 'Tegner',
            'descr': 'Tegner at PDC',
            'hostnames': ['\s*\.*?tegner.*'],
            'modules_system': 'tmod',
            'partitions': [
                {
                    'name': 'login',
                    'scheduler': 'local',
                    'launcher': 'local',
                    'environs': ['builtin'],
                },
                {
                    'name': 'interactive_no_gmx_module',
                    'scheduler': 'local',
                    'launcher': 'mpirun',
                    'environs': ['ompi_3_0'],
                },
                {
                    'name': 'interactive_gmx_module',
                    'scheduler': 'local',
                    'launcher': 'mpirun',
                    'environs': ['gromacs_2020_1_avx2'],
                },
                {
                    'name': 'interactive_gmx_module_gpu',
                    'scheduler': 'local',
                    'launcher': 'mpirun',
                    'environs': ['gromacs_2020_1_avx2'],
                    'resources': [
                            {
                                # This is not necessary in case of interactive
                                # run on Cluster as the interactive node already
                                # been allocated with gpu
                                'name': 'gpu',
                                'options': ['--gres=gpu:K80:1'],
                            }
                    ],
                },
                {
                    'name': 'queue',
                    'scheduler': 'slurm',
                    'launcher': 'mpirun',
                    'access': ['-A pdc.staff'],
                    'environs': ['ompi_3_0'],
                },
            ],
        },
    ],
    'environments': [
        {
            'name': 'ompi_3_0',
            'modules': ['gcc/7.2.0', 'openmpi/3.0-gcc-7.2'],
        },
        {
            'name': 'gromacs_2020_1_avx2',
            'modules': ['gromacs/2020.1-avx2']
        },
        {
            'name': 'gromacs_2020_4',
            'modules': ['gromacs/2020.4']
        },
        {
            'name': 'builtin',
            'cc': 'cc',
            'cxx': '',
            'ftn': '',
        },
    ],
    'logging': [
        {
            'level': 'debug',
            'handlers': [
                {
                    'type': 'stream',
                    'name': 'stdout',
                    'level': 'info',
                    'format': '%(message)s'
                },
                {
                    'type': 'file',
                    'name': 'reframe.log',
                    'level': 'debug',
                    'format': '[%(asctime)s] %(levelname)s: %(check_info)s: %(message)s',   # noqa: E501
                    'append': False
                }
            ],
            'handlers_perflog': [
                {
                    'type': 'filelog',
                    'prefix': '%(check_system)s/%(check_partition)s',
                    'level': 'info',
                    'format': (
                        '%(check_job_completion_time)s|reframe %(version)s|'
                        '%(check_tags)s|%(check_info)s|'
                        # 'jobid=%(check_jobid)s|'
                        '%(check_perf_var)s=%(check_perf_value)s|'
                        'ref=%(check_perf_ref)s '
                        '(l=%(check_perf_lower_thres)s, '
                        'u=%(check_perf_upper_thres)s)|'
                        '%(check_perf_unit)s'
                    ),
                    'append': True
                }
            ]
        }
    ],
}
