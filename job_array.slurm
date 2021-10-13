#!/bin/bash
#SBATCH --job-name={name}            # create a short name for your job
#SBATCH --output={name}_%A.%a.out     # stdout file
#SBATCH --error={name}_%A.%a.out      # stderr file
#SBATCH --nodes={node}               # node count
#SBATCH --ntasks={ntasks}            # total number of tasks across all nodes
#SBATCH --cpus-per-task={cpus}       # cpu-cores per task (>1 if multi-threaded tasks)
#SBATCH --mem-per-cpu={mem_per_cpu}G # memory per cpu-core (4G is default)
#SBATCH --gres=gpu:{gpus}            # number of gpus per node
#SBATCH --time={time}                # total run time limit (HH:MM:SS)
#SBATCH --array={arrays}             # job array with index values 0, 1, 2, 3, 4
#SBATCH --mail-type=all              # send email on job start, end and fault
#SBATCH --mail-user={email}

module purge
module load anaconda3/2021.5

__conda_setup="$('/usr/licensed/anaconda3/2021.5/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/usr/licensed/anaconda3/2021.5/etc/profile.d/conda.sh" ]; then
        . "/usr/licensed/anaconda3/2021.5/etc/profile.d/conda.sh"
    else
        export PATH="/usr/licensed/anaconda3/2021.5/bin:$PATH"
    fi
fi
unset __conda_setup

echo "My SLURM_ARRAY_JOB_ID is $SLURM_ARRAY_JOB_ID."
echo "My SLURM_ARRAY_TASK_ID is $SLURM_ARRAY_TASK_ID"
echo "Executing on the machine:" $(hostname)
