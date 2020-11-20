'''
    Author:
        * Muhammed Ahad <ahad3112@yahoo.com, maaahad@gmail.com, maaahad@kth.se>
    Desctiption:
        -------------
'''
# Python std
import os
import json

# ReFrame

# in-house

class GMXPerformanceReport:
    def __init__(self, test, outputdir):
        reports_dir = os.path.join(
             outputdir,
            (f'reports/{test.gromacs_info["version"]}/'
             f'{test.current_system.name}/{test.current_partition.name}')
        )
        if not os.path.exists(reports_dir):
            os.system(f'mkdir -p {reports_dir}')

        self.__report_file = os.path.join(reports_dir, f'{test.id}.json')
        self.__report = {
            'meta': {
                'name': test.info(),
                'id': test.id,
            },
            'machine': test.machine_info,
            'binaries': test.binaries_info,
            'compilers': test.compilers_info,
            'libraries': test.libraries_info,
            'input': test.sim_input_info,
            # 'output dir': test.storage,
            'gmx_log_info': test.gmx_log_info,
            'performance': test.performance_info
        }


    def dump(self):
        with open(self.__report_file, 'w') as f:
            json.dump(self.__report, f, indent='\t')
