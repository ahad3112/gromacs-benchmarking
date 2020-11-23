# Benchmarking Tool for GROMACS

## Dependencies

* `Python 3.6 of above`
* [ReFrame](https://reframe-hpc.readthedocs.io/en/stable/index.html)

###### Installation of [ReFrame](https://reframe-hpc.readthedocs.io/en/stable/index.html) with `pip`
    pip install reframe-hpc

---

## Usage of `gmxbm.py`
### `run` module
The job of this module is to generate appropriate test cases based on the user's input and initiate [ReFrame](https://reframe-hpc.readthedocs.io/en/stable/index.html) to start benchmarking.

The usage of the tools is done in two steps as follows:

1. Configuring Machine settings.
2. Running `gmxbm.py` with command line arguments.

#### Configuring Machine Settings
`Cluster`, `partition`, `programming environments` for each benchmark test all are set by users in the machine Configuration file. This can be hardcoded in the file `configurations/config.py`. Or, users can provide their own machine configuration file as well using `-C/--config-file` command line argument of `gmxbm.py`. The configuration file has to be hardcoded using the specifications defined by [ReFrame Configuring Site](https://reframe-hpc.readthedocs.io/en/stable/configure.html).

#### Running gmxbm.py

    $ ./gmxbm.py run -h/--help
    usage: ./gmxbm.py run [-h] -i INPUT [-C CONFIG_FILE]
                        [--machines [cluster:partition [cluster:partition ...]]]
                        [--prog-envs [PROG_ENVS [PROG_ENVS ...]]]
                        [--nnodes NNODES] [--nprocs NPROCS] [--ntomp NTOMP]
                        [--gpu] [--mpi] [--envs [name:value [name:value ...]]]
                        [--prepend-env] [--outputdir OUTPUTDIR]
                        [--wall-time <days>d<hours>h<minutes>m<seconds>s] --gmx
                        GMX [--descr DESCR]
                        [--maintainers [MAINTAINERS [MAINTAINERS ...]]]

It is possible to run multiple test based on the `cluster`, `partition` and `programming environment` choices. This is enabled by excepting multiple values for `--machines` and `--prog-envs` options. A new test instance will be generated for each combination of --`--machines` and `--prog-envs` value.

---

# Outputs
By default, all the outputs from the tests are stored in the working directory from where the top level script `gmxbm.py` is run. However, users can specify specific root of the output directory by using the `--outputdir` option while running `gmxbm.py`. If the root of the output directory already contains results from previous tests, new test results will be automatically aggregated alongside that.

List of generated folders within output root:

1. `perflogs`
2. `reports`
3. `gmx-outputs`
4. `logs`

#### `perflogs`
This directory is generated by [ReFrame](https://reframe-hpc.readthedocs.io/en/stable/index.html) and the `GromacsRegressionTest.log` file within the directory contains single liner record for each tests ran using the same `cluster` and `partition` combination. Tree view of the `perflogs` directory:

```
perflogs
└─── cluster_name
│   └─── partition_name
│       └─── GromacsRegressionTest.log
└─── cluster_name
|    └─── partition_name
|        └─── GromacsRegressionTest.log
```


#### `reports`
This directory is generated by `gmxbm.py` and contains in-depth report for each test. This directory structure is as `perflogs` folder except that nesting directories start with `GROMACS` version, followed by `cluster` and `partition` name and for each test there will be one `JSON` formatted file named after the `id` of the test. `id` of the test is generated using the combined hash of `GMX` binary, `libgromacs` and test start time in milliseconds as follows:

`<combined hash of gmx binary and libgromacs>_<hash of test start time in milliseconds>`

Tree view of the `reports` directory:

```
reports
└─── gromacs_version
│   └─── cluster_name
│       └─── partition_name
│           └─── <test_id>.json
│           └─── <test_id>.json
└─── gromacs_version
│   └─── cluster_name
│       └─── partition_name
│           └─── <test_id>.json
│           └─── <test_id>.json
```


#### `gmx-outputs`
This directory contains all the output generated by `GROMACS`. Structure of this directory is similar to `reports`, except that in this case test `id` is used to create folder within `cluster` directory and contains the `GROMACS` output. Tree view of the `gmx-outputs` directory:

```
gmx-outputs
└─── gromacs_version
│   └─── cluster_name
│       └─── partition_name
│           └─── <test_id>
│               └─── gmx_md.log
│               └─── gmx_md.edr
│               └─── gmx_md.gro
│               └─── gmx_md.cpt
│               └─── gmx_md.xtc
└─── gromacs_version
│   └─── cluster_name
│       └─── partition_name
│           └─── <test_id>
│               └─── gmx_md.log
│               └─── gmx_md.edr
│               └─── gmx_md.gro
│               └─── gmx_md.cpt
│               └─── gmx_md.xtc
```

#### `logs`
This folder contains the following temporary files that will be overriden or deleted during/after each test:

1. `kill-reframe.sh`
2. `reframe.log`
3. `reframe.out`

`gmxbm.py` makes [ReFrame](https://reframe-hpc.readthedocs.io/en/stable/index.html) to run on the background. `kill-reframe.sh` allows a user to kill a test prematurely that is runing on background.

`reframe.log` is generated by [ReFrame](https://reframe-hpc.readthedocs.io/en/stable/index.html) contains runtime log from [ReFrame](https://reframe-hpc.readthedocs.io/en/stable/index.html). Initially the file resides in the output directory and is moved to `logs` folder within output directory once [ReFrame](https://reframe-hpc.readthedocs.io/en/stable/index.html) return from execution.

The content of `reframe.out` is the `stdout` message from [ReFrame](https://reframe-hpc.readthedocs.io/en/stable/index.html).


In addition to the above folders, [ReFrame](https://reframe-hpc.readthedocs.io/en/stable/index.html) also generates two temporary folders named `stage` and `output` within the output directory. `stage` folders contains generated job related scripts and output from `GROMACS`. Once the test is done, job related scripts are moved to `output` directory and `GROMACS` outputs are deleted.

### `aggregate` module
The job of this module is to aggregate benchmark results from multiple directories ito a single user specified directory. The ultimate goal with this module is to perform a cron job for data aggregation.

This module accepts a space separated list of input directoris and an output directory.

    $ ./gmxbm.py aggregate -h/--help
    usage: ./gmxbm.py aggregate [-h] [-i INPUTS [INPUTS ...]] -o OUTPUT
