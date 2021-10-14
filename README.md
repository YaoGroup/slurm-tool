# Fast Slurm Jobs Submiision using Princeton Cluster
author: Ming-Ruey(Ray) Chou

A tool auto-generates .slurm script for batch launching jobs using Python.

For exampple, if one has a script `my-job.py`, which includes a independent variable `H` and wants to run the script concurrently with different `H` values:

```bash
python3 ~/my-code/my-job.py H_1
python3 ~/my-code/my-job.py H_2
python3 ~/my-code/my-job.py H_3
python3 ~/my-code/my-job.py H_4
```

One can use the tool to write a single Python file to launch all the jobs on cluster like this:
```python
from slurm_tool import JobArray

jobs = JobArray(name="vary-H-experiments", output_dir="/scratch/gpfs/mc4536", node=1, cpus=1, arrays=5, time=0.5)
jobs.set_env("tf24")
jobs.submit(
    "python3 ~/my-code/my-job.py H_1"
    "python3 ~/my-code/my-job.py H_2"
    "python3 ~/my-code/my-job.py H_3"
    "python3 ~/my-code/my-job.py H_4"
    "python3 ~/my-code/my-job.py H_5"
)
```

## Limitations
- Currently, the features of the tool are still limited to Slrum job-array
- Only supports Conda environment.
- The Python script must accept an `-o` options for specifying the output directory `python3 -o output-dir my-job.py param1 param2`.

## Pre-Steps
- Login to the Cluster
- Create your environment using Conda
- Clone both this tools and your target project from GitHub
- Create a script for job_array, like the example given above
    - Make sure the location which you clone the tools to allow you conduct a `import slurm_tool`
    - Make sure the environment name you use for `.set_env("my-env")` also works from terminal: `conda activate my-env`
- After the `.submit()`, it submit the jobs to the cluster and the auto-generated `.slurm` file is created to the `output_dir` parameter given to `JobArray`
