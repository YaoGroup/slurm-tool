from datetime import datetime

from dataclasses import dataclass, fields
from pathlib import Path
from typing import List

from shell_cmd import ShellCmd, ShellPopenWrapper


def _check_min(val, min, name: str = None):
    assert val > min, f"{name} expects to be larger than {min}"


def poka_yoke(jobs: List[str]):
    for job in jobs:
        if job.count("python") > 1:
            msg = "Detect single job contains two 'python' ({job})"
            print(msg)
            while True:
                answer = input("Could be typo. Still continue anyway? (y/n)")
                if answer.lower() in {"y", "yes"}:
                    return
                elif answer.lower() in {"n", "no"}:
                    raise RuntimeError("User stops the job submitting")


@dataclass
class SlurmConfig:
    name: str
    email: str
    output_dir: str
    time: float
    arrays: int
    node: int = 1
    ntasks: int = 1
    cpus: int = 1
    gpus: int = 1
    mem_per_cpu: int = 4

    def __post_init__(self):
        for field in fields(self):
            if not field.init:
                continue

            value = getattr(self, field.name)
            if not isinstance(value, field.type):
                msg = f"Expected {self.__class__.__name__}" + \
                    f"field {field.name}" + \
                    f"to be {field.type}, got {repr(value)}"
                raise ValueError(msg)

        _check_min(self.arrays, 0)
        _check_min(self.cpus, 0)
        _check_min(self.node, 0)
        _check_min(self.mem_per_cpu, 0)
        _check_min(self.time, 0.0)
        _check_min(self.ntasks, 0)

        self.arrays = f"0-{self.arrays}"
        hour = int(self.time)
        minutes = int((self.time % 1) * 60)
        seconds = int(((self.time % 1) * 60 % 1) * 60)
        self.time = f"{hour}:{minutes:02d}:{seconds:02d}"


    def create_header(self, slurm_template: str) -> str:
        with open(slurm_template, "r") as f:
            txt = f.read()
            lines = []
            configs = {f.name : getattr(self, f.name) for f in fields(self)}
            for line in txt.splitlines():
                if line.startswith("#SBATCH --mail") and not self.email:
                    continue;
                lines.append(line.format(**configs))
            return "\n".join(lines)


class JobArray:

    SLURM_TEMPLATE = Path(__file__).parent.joinpath("job_array.slurm")

    # path for save auto generated slurm script
    SLURM_SCRIPT = Path.cwd().joinpath("{name}_{info}.slurm")

    def __init__(self, **kwargs):
        self._config = SlurmConfig(**kwargs)
        self._conda_env = ""

    @property
    def config(self):
        return self._config

    def set_env(self, conda_env: str):
        """Configure Conda environemtn"""
        self._conda_env = str(conda_env)
        self._config.conda_environemnt = self._conda_env

    def submit(self, jobs: List[str], store_script_as: str = ""):
        """
        Submit the slurm jobs

        Args:
            jobs (List[str]):
                a list of CLI commands to submit, for example,
                ["python3 script.py param1 param2", "python3 script.py param3 param4"]
            store_script_as (str):
                the path to store the auto-generated slurm script, if empty, a default file name is generated.
        """
        # mistake-proofing
        poka_yoke(jobs)

        # test if environemtn works
        cmd = ShellCmd("module purge")
        cmd = cmd.chain(ShellCmd("module load anaconda3/2021.5"))
        cmd = cmd.chain(ShellCmd(f"conda activate {self._conda_env}"))
        if not cmd.execute():
            raise RuntimeError(f"Test initialization of env '{self._conda_env}' failed")

        if not self.SLURM_TEMPLATE.is_file():
            msg = f"Can not find slurm script {self.SLURM_TEMPLATE}"
            raise FileNotFoundError(msg)

        header = self._config.create_header(self.SLURM_TEMPLATE)
        outf = store_script_as
        if not outf:
            info = datetime.now().strftime("%Y%m%d%H%M")
            cnt = 0
            outf = str(self.SLURM_SCRIPT).format(info=info, name=self.config.name)
            while (outf := Path(outf)).is_file():
                outf = str(self.SLURM_SCRIPT).format(info=info + f"_{cnt}")
                cnt += 1

        with open(outf, "w") as f:
            f.write(header + "\n")
            if self._conda_env:
                f.write(f"conda activate {self._conda_env}\n")
            for job in jobs:
                f.write(job + "\n")

        with ShellPopenWrapper() as shell:
            shell.execute(f"sbatch {outf}")
