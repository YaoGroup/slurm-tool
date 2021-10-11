from dataclasses import dataclass, fields
from pathlib import Path
from typing import List

from shell_cmd import ShellCmd


@dataclass
class SlurmConfig:
    name: str
    output_file: str
    node: int
    cpus: int
    gpus: int
    mem_per_cpu: int
    time: float
    email: str

    def __post_init__(self):
        for field in fields(self):
            value = getattr(self, field.name)
            if not isinstance(value, field.type):
                msg = f"Expected {self.__class__.__name__}" + \
                    f"field {field.name}" + \
                    f"to be {field.type}, got {repr(value)}"
                raise ValueError(msg)


class JobArray:

    SLURM_SCRIPT = Path(__file__).parent.joinpath("slurm-script_job-array.sh")

    def __init__(self, **kwargs):
        self._config = SlurmConfig(**kwargs)
        self.modules = []
        self.presteps = []

    @property
    def config(self):
        return self._config

    def module_load(self, modules: List[str]):
        for module in modules:
            cmd = ShellCmd("module load " + module)
            # if test load success, add them into final config
            if cmd.execute():
                self.modules.append(cmd)

    def add_prestep(self, cmd: str):
        # if test load success, add it into final config
        cmd = ShellCmd(str(cmd))
        if cmd.execute():
            self.presteps.append(cmd)

    def submit(self, jobs: List[str]):
        pass
