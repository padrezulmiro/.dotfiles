#!/usr/bin/env python3

# TODO(azul):
# 1. Add a dry run option
# 2. Check for click's installation

import click
import subprocess
import pexpect
import logging
from typing import int

esc_code = "\033["
del_line_code = esc_code + "2K"
cursor_up_code = esc_code + "A"
cursor_down_code = esc_code + "B"

log_file = "install.log"


# ****************** CONSOLE ESCAPE CODE HELPERS ******************************


def del_line_at_cursor() -> None:
    """Delete line at console's cursor"""
    click.echo(del_line_code, nl=False)


def move_cursor_up(num_lines: int = 1) -> None:
    """Move cursor num_lines up."""
    if num_lines == 1:
        click.echo(cursor_up_code, nl=False)
    elif num_lines > 1:
        code = esc_code + str(num_lines) + "A"
        click.echo(code, nl=False)


def move_cursor_down(num_lines: int = 1) -> None:
    """TODO"""
    if num_lines == 1:
        click.echo(cursor_down_code, nl=False)
    elif num_lines > 1:
        code = esc_code + str(num_lines) + "B"
        click.echo(code, nl=False)


def del_lines_above(n_lines: int = 0) -> None:
    """TODO"""
    if n_lines >= 0:
        del_line_at_cursor()
    if n_lines > 0:
        for i in range(n_lines):
            move_cursor_up()
            del_line_at_cursor()


# ****************** LOGGING HELPERS ******************************************


def init_logger(log_level: int = logging.INFO) -> logging.Logger:
    """TODO"""
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)

    handler = logging.FileHandler(log_file, encoding="utf-8")
    handler.setLevel(log_level)

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelno)s: %(message)s",
        datefmt="%d/%m/%y, %H:%M:%S"
    )

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


def log_and_echo(logger: logging.Logger, log_level: int, message: str) -> None:
    logger.log(log_level, message)
    click.echo(message)


# ****************** CLI TOOLS HELPERS ****************************************


def grep(grep_input: str, search_token: str) -> str:
    """Pipe grep_input to a grep process, and search for search_token"""
    cmd_grep = ["grep", search_token]
    res_grep = subprocess.run(cmd_grep, capture_output=True, text=True,
                              input=grep_input)
    return res_grep.stdout


def aptget_install(pkg: str):
    """Run an apt-get process to install pkg"""
    child = pexpect.spawn()
    pass


def dpkg_is_pkg_installed(pkg: str) -> bool:
    """Confirm whether pkg is installed using Debian's dpkg"""
    res = subprocess.run(
        ["dpkg-query", "-W", pkg],
        capture_output=True,
        text=True
    )
    is_installed = len(res.stdout) != 0
    return is_installed


# ****************** INSTALLERS ***********************************************


def ubuntu_install_programs():
    """TODO"""

    # Confirm root access privileges
    # if os.geteuid() != 0:
    #     click.echo("This script requires root-level access. Please run it " +
    #                "with sudo.")
    #     sys.exit(1)

    click.echo("Installing utilities...")

    # TODO(azul) Install zsh
    is_zsh_installed = dpkg_is_pkg_installed("zsh")
    if is_zsh_installed:
        click.echo("zsh is already installed!")
    else:
        click.echo("zsh is not installed!")

    # XXX(azul) Testing installation

    # TODO(azul) Install oh-my-zsh

    # TODO(azul) Install emacs

    # TODO(azul) Install doom-emacs

    click.echo("This installation script is a WIP")


# ****************** CLI DEFINITIONS ******************************************


@click.group()
def main():
    pass


@main.command()
def ubuntu():
    """Installs these dotfiles on Ubuntu-like distributions"""
    ubuntu_install_programs()


if __name__ == "__main__":
    main()
