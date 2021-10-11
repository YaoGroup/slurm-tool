import sys
from pathlib import Path
import pytest

root = Path(__file__).parent.parent
sys.path.append(str(root))

from shell_cmd import ShellCmd, ShellCmdChain


class TestShellCmd:

    def test_cmd_execute(self):
        echo = ShellCmd("echo Hello World")
        assert echo.execute()

    def test_cmd_chain(self):
        echo1 = ShellCmd("echo Hello World")
        echo2 = ShellCmd("echo Hello Princeton")
        chain = echo1.chain(echo2)
        assert chain.execute()



if __name__ == "__main__":
    pytest.main(["-s", "-v", __file__])