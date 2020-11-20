```Usage```

NOTE:
[2020-11-16T15:15:53] debug: GromacsRegressionTest on Beskow:queue using gromacs20204: executing OS command: modulecmd python show gromacs/2020.4
[2020-11-16T15:15:53] debug: GromacsRegressionTest on Beskow:queue using gromacs20204: executing OS command: modulecmd python load gromacs/2020.4


<!-- TESTING NEW IMPLEMENTATION on Tegner-->
<!-- With container -->
./gmx-bm/gmxbm.py run --input '/cfs/klemming/nobackup/m/maaahad/gromacs/test-run/no-singularity/tegner/2020.1-avx2/topol-2020.1.tpr' --nprocs 4 --machines Tegner:interactive --mpi --container singularity --img '/cfs/klemming/nobackup/m/maaahad/gromacs/singularity/images/gromacs-2020.1-gcc-7-cmake-3.17.1-ompi-3.0.0-fftw-3.3.7.sif' --ntomp 6 --outputdir /cfs/klemming/nobackup/m/maaahad/gromacs/benchmark/tools/tegner_container_test/


./gmxbm.py run --input '/cfs/klemming/nobackup/m/maaahad/gromacs/test-run/no-singularity/tegner/2020.1-avx2/topol-2020.1.tpr' --nprocs 4 --machines Tegner:interactive --mpi --wall-time 5h30m20s --ntomp 6 --gmx test

<!-- Without container / without gpu / without module-->
./gmx-bm/gmxbm.py run --input '/cfs/klemming/nobackup/m/maaahad/gromacs/test-run/no-singularity/tegner/2020.1-avx2/topol-2020.1.tpr' --nprocs 4 --machines Tegner:interactive_no_gmx_module --mpi --ntomp 6 --outputdir /cfs/klemming/nobackup/m/maaahad/gromacs/benchmark/tools/tegner_test/ --gmx gmx_mpi --envs PATH:/afs/pdc.kth.se/home/m/maaahad/gromacs/installation/.gromacs-2020.1/bin LD_LIBRARY_PATH:/afs/pdc.kth.se/home/m/maaahad/gromacs/installation/.gromacs-2020.1/lib64

<!-- Without container / without gpu / with module-->
./gmx-bm/gmxbm.py run --input '/cfs/klemming/nobackup/m/maaahad/gromacs/test-run/no-singularity/tegner/2020.1-avx2/topol-2020.1.tpr' --nprocs 4 --machines Tegner:interactive_module --mpi --ntomp 6 --outputdir /cfs/klemming/nobackup/m/maaahad/gromacs/benchmark/tools/tegner_test/ --gmx gmx_mpi --envs PATH:/pdc/vol/gromacs/2020.1/amd64_co7/haswell/bin

<!-- Without container / with gpu / with module-->
./gmx-bm/gmxbm.py run --input '/cfs/klemming/nobackup/m/maaahad/gromacs/test-run/no-singularity/tegner/2020.1-avx2/topol-2020.1.tpr' --nprocs 4 --machines Tegner:interactive_gmx_module Tegner:interactive_gmx_module_gpu --mpi --ntomp 6 --outputdir /cfs/klemming/nobackup/m/maaahad/gromacs/benchmark/tools/tegner_mult_test/ --gmx gmx_mpi --gpu

<!-- Without container / with gpu-->
./gmx-bm/gmxbm.py run --input '/cfs/klemming/nobackup/m/maaahad/gromacs/test-run/no-singularity/tegner/2020.1-avx2/topol-2020.1.tpr' --nprocs 4 --machines Tegner:interactive --mpi --ntomp 6 --outputdir /cfs/klemming/nobackup/m/maaahad/gromacs/benchmark/tools/tegner_test/ --gmx gmx_mpi --envs PATH:/afs/pdc.kth.se/home/m/maaahad/gromacs/installation/.gromacs-2020.1/bin PATH:/afs/pdc.kth.se/home/m/maaahad/gromacs/installation


<!-- hexdigest of /afs/pdc.kth.se/home/m/maaahad/gromacs/installation/.gromacs-2020.1 bin(gmx_mpi) and libgromacs_mpi-->
'eb1c2c29a416c3d10922ee1ad19d6f69'

<!-- TESTING NEW IMPLEMENTATION on Beskow-->
Combined hash for Gromaca binary and libgromacs:  'bee3ffdc19585451df2cfc880fa34819'

<!-- Interactive  + Without gpu / with module -->
./gmx-bm/gmxbm.py run --input '/cfs/klemming/nobackup/m/maaahad/gromacs/test-run/no-singularity/tegner/2020.1-avx2/topol-2020.1.tpr' --nprocs 4 --machines Beskow:interactive_module --mpi --ntomp 6 --outputdir /cfs/klemming/nobackup/m/maaahad/gromacs/benchmark/tools/beskow_test/ --gmx gmx_mpi

<!-- QUEUE  + Without gpu / with module / single node-->
./gmx-bm/gmxbm.py run --input '/cfs/klemming/nobackup/m/maaahad/gromacs/test-run/no-singularity/tegner/2020.1-avx2/topol-2020.1.tpr' --nprocs 4 --machines Beskow:queue --mpi --ntomp 6 --outputdir /cfs/klemming/nobackup/m/maaahad/gromacs/benchmark/tools/beskow_test/ --gmx gmx_mpi --wall-time 1h

<!-- QUEUE  + Without gpu / with module / multiple node-->
./gmx-bm/gmxbm.py run --input '/cfs/klemming/nobackup/m/maaahad/gromacs/test-run/no-singularity/tegner/2020.1-avx2/topol-2020.1.tpr' --nprocs 16 --nnodes 2 --machines Beskow:queue --mpi --ntomp 6 --outputdir /cfs/klemming/nobackup/m/maaahad/gromacs/benchmark/tools/beskow_test/ --gmx gmx_mpi --wall-time 1h




TEGNER

WORKING: Sample command to run on Tegner with singularity on interactive node:

    ./gmxbm.py run --input '/cfs/klemming/nobackup/m/maaahad/gromacs/test-run/no-singularity/tegner/2020.1-avx2/topol-2020.1.tpr' --systems Tegner:login --container singularity --img '/cfs/klemming/nobackup/m/maaahad/gromacs/singularity/images/gromacs-2020.1-gcc-7-cmake-3.17.1-ompi-3.0.0-fftw-3.3.7.sif' --wall-time 5h30m20s
    ./gmxbm.py run --input '/cfs/klemming/nobackup/m/maaahad/gromacs/test-run/no-singularity/tegner/2020.1-avx2/topol-2020.1.tpr' --systems Tegner:interactive --container singularity --img '/cfs/klemming/nobackup/m/maaahad/gromacs/singularity/images/gromacs-2020.1-gcc-7-cmake-3.17.1-ompi-3.0.0-fftw-3.3.7.sif' --wall-time 5h30m20s


    ./gmxbm.py run --input '/cfs/klemming/nobackup/m/maaahad/gromacs/test-run/no-singularity/tegner/2020.1-avx2/topol-2020.1.tpr' --systems Tegner:interactive --mpi --container singularity --img '/cfs/klemming/nobackup/m/maaahad/gromacs/singularity/images/gromacs-2020.1-gcc-7-cmake-3.17.1-ompi-3.0.0-fftw-3.3.7.sif' --wall-time 5h30m20s

    <!-- mpi with np = 4 without gpu-->
    ./gmxbm.py run --input '/cfs/klemming/nobackup/m/maaahad/gromacs/test-run/no-singularity/tegner/2020.1-avx2/topol-2020.1.tpr' -np 4 --systems Tegner:interactive --mpi --container singularity --img '/cfs/klemming/nobackup/m/maaahad/gromacs/singularity/images/gromacs-2020.1-gcc-7-cmake-3.17.1-ompi-3.0.0-fftw-3.3.7.sif' --wall-time 5h30m20s --ntomp 6 --performance-report


    <!-- mpi with np = 4 with gpu-->
    ./gmxbm.py run --input '/cfs/klemming/nobackup/m/maaahad/gromacs/test-run/no-singularity/tegner/2020.1-avx2/topol-2020.1.tpr' -np 4 --systems Tegner:interactive --mpi --container singularity --img '/cfs/klemming/nobackup/m/maaahad/gromacs/singularity/images/gromacs-2020.1-gcc-7-cmake-3.17.1-ompi-3.0.0-fftw-3.3.7-cuda-10.0.sif' --gpu --wall-time 5h30m20s --ntomp 6 --performance-report

    ./gmxbm.py run --input '/cfs/klemming/nobackup/m/maaahad/gromacs/test-run/no-singularity/tegner/2020.1-avx2/topol-2020.1.tpr' -np 4 --systems Tegner:interactive --mpi --container singularity --img '/cfs/klemming/nobackup/m/maaahad/gromacs/singularity/images/gromacs-2020.1-gcc-7-cmake-3.17.1-ompi-3.0.0-fftw-3.3.7.sif' --wall-time 5h30m20s --ntomp 6 --performance-report

Sample command to run on Tegner without singularity in login + interactive nodes:

    ./gmxbm.py run --input '/cfs/klemming/nobackup/m/maaahad/gromacs/benchmark/gromacs/g2020.1.tpr' -np 4 --ntomp 6 --mpi --systems Tegner:interactive --envs PATH:/afs/pdc.kth.se/home/m/maaahad/gromacs/installation/.gromacs-2020.1/bin LD_LIBRARY_PATH:/afs/pdc.kth.se/home/m/maaahad/gromacs/installation/.gromacs-2020.1/lib64


Sample command to run on Tegner with singularity using Queue system:

    ./gmxbm.py run --input '/cfs/klemming/nobackup/m/maaahad/gromacs/test-run/no-singularity/tegner/2020.1-avx2/topol-2020.1.tpr' -np 4 --systems Tegner:queue --mpi --container singularity --img '/cfs/klemming/nobackup/m/maaahad/gromacs/singularity/images/gromacs-2020.1-gcc-7-cmake-3.17.1-ompi-3.0.0-fftw-3.3.7.sif' --wall-time 5h30m20s


BESKOW

Sample command to run on Beskow without singularity in login + interactive nodes:

    ./gmxbm.py run --input /cfs/klemming/nobackup/m/maaahad/gromacs/benchmark/gromacs/g2020.1.tpr --ntomp 6 --mpi --systems Beskow:interactive --envs PATH:/cfs/klemming/nobackup/m/maaahad/gromacs/installation/.gromacs-2020.3/bin LD_LIBRARY_PATH:/cfs/klemming/nobackup/m/maaahad/gromacs/installation/.gromacs-2020.3/lib64


Sample command to run on Beskow without singularity using Queue system:

    ./gmxbm.py run --input /cfs/klemming/nobackup/m/maaahad/gromacs/benchmark/gromacs/g2020.1.tpr --ntomp 6 --mpi --systems Beskow:queue --envs PATH:/cfs/klemming/nobackup/m/maaahad/gromacs/installation/.gromacs-2020.3/bin LD_LIBRARY_PATH:/cfs/klemming/nobackup/m/maaahad/gromacs/installation/.gromacs-2020.3/lib64
