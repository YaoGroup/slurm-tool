class ShellCmd:
    """Abstraction of a single line shell command"""
    def __init__(self, cmd: str):
        self.text = cmd

    def execute(self):
        return False
