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
`srun`, though the jupyter commands do some post-processing to help you connect to the
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
instance respectively. After starting the server, `slurmrun` will show a command to set up
an SSH tunnel to the SLURM node and print a URL for you to navigate to in your local
browser, for example

```sh
$ slurmrun lab
# ...
Now open an SSH tunnel to this node:

    ssh -L 8888:gpu07.kdd.in.tum.de:8888 fs

Then access the following URL in your browser:

    http://localhost:8888/lab?token=599fef63cd7b7834771f945410e332a1d96caa0dae010a5e
```

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
