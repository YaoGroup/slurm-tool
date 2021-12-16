# Fast Slurm Jobs Submission using Princeton Cluster
author: Ming-Ruey(Ray) Chou

A tool auto-generates .slurm script for batch launching jobs using Python.

## Before Use:

You have to understand how to submit a job to Slurm.
We highly recommend going through the guide from Princeton Research Computing:

https://researchcomputing.princeton.edu/get-started/guide-princeton-clusters
https://researchcomputing.princeton.edu/support/knowledge-base/slurm

If you are impatient, you can directly jump to the Python page:
https://researchcomputing.princeton.edu/support/knowledge-base/python

## Usage:

For example, the [`script_inverse.py`](https://github.com/YaoGroup/IceShelf2D/blob/main/script/script_inverse.py) in our Shelf 2D project receive the value of the interested parameter `noise_ratio` from command line, and also the directory for output the files via `-o` options:

```bash
python ~/IceShelf2D/script/script_inverse.py 0.01 -o /scratch/gpfs/mc4536
```
which means, the `script_inverse.py` is written in the way so that it will use `0.01` as the value of `noise_value`, and will store its output to `/scratch/gpfs/mc4536`. 
For more information about how to make such script, please refer to [Python built-in libaray argparse](https://docs.python.org/3/library/argparse.html).

Using terminal to systematically experiment with different values of `noise_ratio`, one can do:
```bash
# this is bash
python ~/IceShelf2D/script/script_inverse.py 0.01 -o /scratch/gpfs/mc4536 &&
python ~/IceShelf2D/script/script_inverse.py 0.05 -o /scratch/gpfs/mc4536 &&
python ~/IceShelf2D/script/script_inverse.py 0.1 -o /scratch/gpfs/mc4536 &&
python ~/IceShelf2D/script/script_inverse.py 0.5 -o /scratch/gpfs/mc4536 &&
...
```
One can use our tool (which is in Python) to generate the slurm script for above jobs, and submit the script to Princeton cluster:
```python
# this is Python file called `my_submit.py`
from slurm_tool import JobArray

jobs = JobArray(name="vary-noise-experiments", output_dir="/scratch/gpfs/mc4536", node=1, cpus=1, arrays=5, time=0.5)
jobs.set_env("tf24")
jobs.submit([
    "python ~/IceShelf2D/script/script_inverse.py 0.01",
    "python ~/IceShelf2D/script/script_inverse.py 0.05",
    "python ~/IceShelf2D/script/script_inverse.py 0.1",
    "python ~/IceShelf2D/script/script_inverse.py 0.5",
])
```
Running the above Python file (`python my_submit.py`) will:
- Create a Slurm script for running the 4 jobs and store the script into the `output_dir` of `JobArray`
- Send the script to the cluster, so user DO NOT need to `sbatch` the script themselves.

## Limitations
- Currently, the features of the tool are still limited to Slrum job-array
- Only supports Conda environment.
- The Python script must accept an `-o` options for specifying the output directory `python3 -o output-dir my-job.py param1 param2`.

## Pre-Steps
- Login to the Cluster (for example `ssh mc4536@della.princeton.edu`)
- Create your environment using Conda. Acitvate the environment and test it.
- Clone both this tools and your target project from GitHub
- Create a script for job_array, like the example given above
    - Make sure the location which you clone the tools to allow you conduct a `import slurm_tool`
    - Make sure the environment name you use for `.set_env("my-env")` also works from terminal: `conda activate my-env`
- After the `.submit()`, it submit the jobs to the cluster and the auto-generated `.slurm` file is created to the `output_dir` parameter given to `JobArray`
