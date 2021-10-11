#!/bin/bash
#SBATCH --job-name={name}            # create a short name for your job
#SBATCH --output=slurm-%A.%a.out     # stdout file
#SBATCH --error=slurm-%A.%a.err      # stderr file
#SBATCH --nodes={node}               # node count
#SBATCH --ntasks={ntasks}            # total number of tasks across all nodes
#SBATCH --cpus-per-task={cpus}       # cpu-cores per task (>1 if multi-threaded tasks)
#SBATCH --mem-per-cpu={mem_per_cpu}  # memory per cpu-core (4G is default)
#SBATCH --time={time}                # total run time limit (HH:MM:SS)
#SBATCH --array={arrays}             # job array with index values 0, 1, 2, 3, 4
#SBATCH --mail-type=all              # send email on job start, end and fault
#SBATCH --mail-user={email}

echo "My SLURM_ARRAY_JOB_ID is $SLURM_ARRAY_JOB_ID."
echo "My SLURM_ARRAY_TASK_ID is $SLURM_ARRAY_TASK_ID"
echo "Executing on the machine:" $(hostname)
