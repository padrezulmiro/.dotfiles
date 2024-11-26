#!/usr/bin/env python3

# TODO(azul):
# 1. Add a dry run option
# 2. Check for click's installation

import click
import subprocess
import os
import sys


def ubuntu_install_programs():
    """TODO"""

    # Confirm root access privileges
    if os.geteuid() != 0:
        click.echo("This script requires root-level access. Please run it " +
                   "with sudo.")
        sys.exit(1)

    click.echo("Installing utilities...")

    cmd = ["ls", "-al"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    click.echo(res.stdout)

    # TODO(azul) Install zsh

    # TODO(azul) Install oh-my-zsh

    # TODO(azul) Install emacs

    # TODO(azul) Install doom-emacs

    click.echo("This installation script is a WIP")


@click.group()
def main():
    pass


@main.command()
def ubuntu():
    """Installs these dotfiles on Ubuntu-like distributions"""
    ubuntu_install_programs()


if __name__ == "__main__":
    main()
