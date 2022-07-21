# slurmrun

A frontend for `srun` to help you run [jupyter
lab](https://jupyterlab.readthedocs.io/en/stable/) and get interactive shells on SLURM
compute nodes.

## Installation

We recommend the installation with [pipx](https://github.com/pypa/pipx) to keep `slurmrun`
separate from the rest of your python environment.

```sh
pipx install git+https://github.com/martenlienen/slurmrun.git
```

## Usage

`slurmrun` has multiple subcommands to run different things. In the end, they all defer to
`srun`, though the jupyter commands do some pre-processing to help you connect to the
server.

```sh
slurmrun run|shell|lab|notebook
```

The options for `srun` such as how many GPUs and memory to reserve are read from
`~/.config/slurmrun/settings.toml`. Under the `slurm` key, you can configure any option
that `srun` accepts.

```toml
[slurm]
time = "0-08:00"
cpus-per-task = 2
mem = "16G"
gres = "gpu:1"
partition = "gpu_all"
qos = "interactive"
```

### Jupyter

With `lab` and `notebook` you start a jupyter
[lab](https://jupyterlab.readthedocs.io/en/stable/) or [notebook](https://jupyter.org/)
instance respectively. After starting the server, `slurmrun` will defer to the remote
jupyter instance, which will print a URL for you to open in your browser, such as

```sh
$ slurmrun lab
# ...
    To access the server, open this file in a browser:
        file:///nfs/homedirs/lienen/.config/slurmrun/run/tmpxong3w1o/jupyter/jpserver-3645900-open.html
    Or copy and paste one of these URLs:
# ==>   http://gpu20.daml.in.tum.de:8888/lab?token=93c6cffc2c555117614d2e6f37f1e96d249a968e6565155a
     or http://127.0.0.1:8888/lab?token=93c6cffc2c555117614d2e6f37f1e96d249a968e6565155a
```

The line marked with `==>` is the one you have to access because it contains the external
hostname of the compute node that you can access within the VPN.

### Shell and Other Commands

You can also use `slurmrun` to run arbitrary commands or get an interactive shell.

```sh
$ slurmrun run python -c "import torch; x = torch.randn(1000, device='cuda'); print(x.mean())"
tensor(0.0111, device='cuda:0')

$ hostname
fs
$ slurmrun shell
$ hostname
gpu07 # We are now on a SLURM node
```
