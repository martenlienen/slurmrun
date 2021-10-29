import os
from typing import Dict, List

import click


def to_cmd_args(options: Dict[str, str]) -> List[str]:
    return [f"--{key}={value}" for key, value in options.items()]


def run_command(command: List[str], options: Dict[str, str]):
    pid = os.fork()
    if pid == 0:
        # Replace the parent process with the command, so that the command stays attached
        # to the shell, and return in the child
        return

    args = ["srun", "--pty"] + to_cmd_args(options) + command
    click.secho(" ".join(args), fg="yellow")
    os.execvp("srun", args)
