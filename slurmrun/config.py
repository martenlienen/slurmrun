import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict

import click
import tomli


def config_dir():
    return Path("~/.config/slurmrun/").expanduser()


@dataclass
class Config:
    slurm: Dict[str, str] = field(default_factory=dict)

    @classmethod
    def from_user_settings(cls):
        path = config_dir() / "settings.toml"
        if path.is_file():
            config = tomli.loads(path.read_text())
        else:
            click.secho(f"No configuration file at {path}", fg="red", file=sys.stderr)
            config = {}

        return cls(slurm=config.get("slurm", {}))
