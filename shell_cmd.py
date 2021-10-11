from __future__ import annotations
from typing import List
import logging
import subprocess


class ShellPopenWrapper:

    def __init__(self):
        self.popen = subprocess.Popen("/bin/bash", stdin=subprocess.PIPE)

    def __enter__(self):
        self.popen.__enter__()
        return self

    def execute(self, txt: str, timeout: int = 30) -> bool:
        try:
            bytes = (txt + "\n").encode()
            stdout, stderr = self.popen.communicate(bytes, timeout=timeout)
            if self.popen.returncode != 0:
                logging.error(f"ShellCmd execute failed '{txt}': {stderr}")
                return False
            logging.info(f"ShellCmd '{txt}': {stdout}")
            return True
        except ValueError as err:
            logging.error(f"Invalid ShellCmd argument '{txt}': {err}")
            return False
        except subprocess.TimeoutExpired as err:
            logging.error(f"Execute ShellCmd '{txt}' timeout after {self.timeout}s : {err}")
            return False

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self.popen.__exit__(exc_type, exc_val, exc_tb)


class ShellCmd:
    """Abstraction of a single line shell command"""
    def __init__(self, cmd: str, timeout: int = 30):
        self.text = cmd
        self.timeout = 30

    def execute(self, shell: ShellPopenWrapper = None) -> bool:
        if shell is None:
            with ShellPopenWrapper() as shell:
                return shell.execute(self.text, self.timeout)
        else:
            return shell.execute(self.text)

    def __iter__(self):
        return iter([self])

    def chain(self, other) -> ShellCmdChain:
        return ShellCmdChain(list(self) + list(other))


class ShellCmdChain:
    """Abstraction of a series of shell commands"""

    def __init__(self, cmds: List[ShellCmd]):
        self._cmds = list(cmds)

    def __iter__(self):
        return iter(self._cmds)

    def chain(self, other) -> ShellCmdChain:
        return ShellCmdChain(list(self) + list(other))

    def execute(self, shell : ShellPopenWrapper = None) -> bool:
        txt = ""
        for cmd in self._cmds:
            txt += cmd.text + ";"

        if shell is None:
            with ShellPopenWrapper() as shell:
                return shell.execute(txt)
        else:
            return shell.execute(txt)
