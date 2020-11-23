'''
    Author:
        * Muhammed Ahad <ahad3112@yahoo.com, maaahad@gmail.com, maaahad@kth.se>
    Desctiption:
        -------------
'''

import os
import sys
import glob


def handler(args):
    '''
    For Security purpose, the script should not delete any inputs or output
    directory. User is responsible to clean up his directory
    '''
    #  We alrady have output directory created (by args type or by the user)

    for input_dir in args.inputs:
        os.chdir(input_dir)
        reports = [os.path.split(path)[0] for path in glob.glob('reports/*/*/*/*')]
        gmx_outupts = [os.path.split(path)[0] for path in glob.glob('gmx-outputs/*/*/*/*')]
        perf_logs = glob.glob('perflogs/*/*/*')
        # print(reports, gmx_outupts, perf_logs, sep='\n')

        for (index, data_paths) in enumerate((perf_logs, reports,gmx_outupts)):
            for data in data_paths:
                if index == 0:
                    perf_log_path = os.path.split(data)[0]
                    output_perf_log_path = os.path.join(args.output, perf_log_path)
                    if not os.path.exists(output_perf_log_path):
                        os.system(
                            f'mkdir -p {output_perf_log_path}'
                        )
                        os.system(f'cp {data} {output_perf_log_path}/')

                        if args.verbose:
                            print('[ {0:^10} ] : {1} to {2}/'.format(
                                'copied'.upper(),
                                os.path.join(input_dir, data),
                                output_perf_log_path
                            ))
                    else:
                        file = open(os.path.join(args.output, data), 'a')
                        for line in open(data):
                            file.write(line)

                        if args.verbose:
                            print('[ {0:^10} ] : content of {1} to {2}'.format(
                                'copied'.upper(),
                                os.path.join(input_dir, data),
                                os.path.join(args.output, data)
                            ))
                else:
                    if not os.path.exists(os.path.join(args.output, data)):
                        os.system(f'mkdir -p {os.path.join(args.output, data)}')

                    os.system(f'cp -r {data}/* {os.path.join(args.output, data)}/')

                    if args.verbose:
                        print('[ {0:^10} ] : {1}/* to {2}/'.format(
                            'copied'.upper(),
                            os.path.join(input_dir, data),
                            os.path.join(args.output, data)
                        ))
