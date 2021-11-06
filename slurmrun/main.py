import json
import sys
import tempfile
import time
from pathlib import Path
from urllib.parse import urlparse

import click
import shellingham

from . import srun
from .config import Config, config_dir


class ShellOption(click.Option):
    def get_default(self, ctx: click.Context, call: bool = True):
        name, path = shellingham.detect_shell()
        return path


@click.group(context_settings=dict(help_option_names=["-h", "--help"]))
def main():
    """Run interactive commands on SLURM compute nodes."""
    pass


@main.command(context_settings=dict(ignore_unknown_options=True))
@click.argument("command", nargs=-1, required=True)
def run(command):
    """Run an arbitrary command.

    If you want to pass options to the command itself remember to prepend the command
    with two dashes like

        slurmrun run -- hostname --all-fqdns
    """
    config = Config.from_user_settings()
    srun.run_command(list(command), config.slurm)


@main.command()
@click.option(
    "-s",
    "--shell",
    cls=ShellOption,
    metavar="SHELL",
    help="Shell to run",
    show_default=True,
)
@click.pass_context
def shell(ctx, shell):
    """Run an interactive shell."""
    config = Config.from_user_settings()
    srun.run_command([shell], config.slurm)


def run_jupyter(subcommand, config, timeout=None):
    run_dir = config_dir() / "run"
    run_dir.mkdir(parents=True, exist_ok=True)
    tmpdir = Path(tempfile.mkdtemp(dir=run_dir))
    jp_rundir = tmpdir / "jupyter"
    jp_rundir.mkdir()

    script = f"""#!/bin/bash
hostnames=($(hostname --all-fqdns))
export JUPYTER_RUNTIME_DIR={jp_rundir}
jupyter {subcommand} --no-browser --ip=${{hostnames[0]}}
"""

    script_path = tmpdir / "jupyter.sh"
    script_path.write_text(script)
    script_path.chmod(0o755)

    srun.run_command([str(script_path)], config.slurm)

    start = time.monotonic()
    while len(list(jp_rundir.glob("*server-*.json"))) == 0:
        time.sleep(0.2)
        if timeout is not None and time.monotonic() - start > timeout:
            click.secho(
                f"Waited for jupyter for {timeout} seconds. Aborting!", fg="red"
            )
            return

    for server_file in jp_rundir.glob("*server-*.json"):
        server_cfg = json.loads(server_file.read_text())

        url, port, token = server_cfg["url"], server_cfg["port"], server_cfg["token"]
        url_components = urlparse(url)
        host = url_components.hostname
        scheme = url_components.scheme
        if subcommand == "lab":
            path = "lab"
        else:
            path = ""
        msg = f"""
Now open an SSH tunnel to this node:

    ssh -L {port}:{host}:{port} fs

Then access the following URL in your browser:

    {scheme}://localhost:{port}/{path}?token={token}
"""
        click.secho(msg, fg="yellow", file=sys.stderr)


@main.command()
@click.option("--timeout", type=float, help="How long to wait for jupyter")
def lab(timeout):
    """Run jupyter lab."""
    config = Config.from_user_settings()
    run_jupyter("lab", config, timeout)


@main.command()
@click.option("--timeout", type=float, help="How long to wait for jupyter")
def notebook(timeout):
    """Run jupyter notebook."""
    config = Config.from_user_settings()
    run_jupyter("notebook", config, timeout)
