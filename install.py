#!/usr/bin/env python3

# TODO(azul):
# 1. Add a dry run option
# 2. Check for click's installation

# TODO(azul) Package wishlist:
# [] ansible
# [x] zsh
# [x] oh-my-zsh
# [x] emacs
# [x] fd-find (doom-emacs dependency)
# [x] ripgrep (doom-emacs dependency)
# [x] zellij
# [x] stow
# [x] htop
# [] some nerd font - FiraCode Nerd Font Mono
# [] starship
# [] doom-emacs
# [] neovim
# [] some neovim starter

import click
import subprocess
import pexpect
import logging
import re
import os
import sys
import typing

ESC_CODE = "\033["
DEL_LINE_CODE = ESC_CODE + "2K"
CURSOR_UP_CODE = ESC_CODE + "A"
CURSOR_DOWN_CODE = ESC_CODE + "B"

LOG_FILE = "install.log"

logger: logging.Logger = None
log_level: int = 0

aptget_packages = [
    "zsh",
    # "oh-my-zsh",
    # "emacs",
]

# ****************** CONSOLE ESCAPE CODE HELPERS ******************************


def del_line_at_cursor() -> None:
    """Delete line at console's cursor"""
    click.echo(DEL_LINE_CODE, nl=False)


def move_cursor_up(num_lines: int = 1) -> None:
    """Move cursor num_lines up."""
    if num_lines == 1:
        click.echo(CURSOR_UP_CODE, nl=False)
    elif num_lines > 1:
        code = ESC_CODE + str(num_lines) + "A"
        click.echo(code, nl=False)


def move_cursor_down(num_lines: int = 1) -> None:
    """Move cursor num_lines down."""
    if num_lines == 1:
        click.echo(CURSOR_DOWN_CODE, nl=False)
    elif num_lines > 1:
        code = ESC_CODE + str(num_lines) + "B"
        click.echo(code, nl=False)


def del_lines_above(n_lines: int = 0) -> None:
    """Delete n_lines above the cursor's line, including the current line"""
    if n_lines >= 0:
        del_line_at_cursor()
    if n_lines > 0:
        for i in range(n_lines):
            move_cursor_up()
            del_line_at_cursor()


# ****************** LOGGING HELPERS ******************************************


def init_logger(log_level: int = logging.INFO) -> logging.Logger:
    """Init logger with log_level level of debugging and with specified
    formatting"""
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)

    handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    handler.setLevel(log_level)

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelno)s: %(message)s",
        datefmt="%d/%m/%y, %H:%M:%S"
    )

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


def log_and_echo(log_level: int, message: str) -> None:
    """Log message with a given log level and echo it via click.echo"""
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
    """Run an apt-get process to install pkg interactively"""
    logger.info("Installing {}".format(pkg))

    aptget_command = "apt-get install " + pkg
    aptget_proc = pexpect.spawn(aptget_command, encoding="utf-8")

    NL = 0
    INTERACT_PROMPT = 1
    EOF = 2
    TIMEOUT = 3
    expect_patterns = [
        "\n",
        "Do you want to continue? \\[Y/n\\]",
        pexpect.EOF,
        pexpect.TIMEOUT
    ]

    # FIXME(azul) Doesn't handle
    # user replying no to the [Y/n] prompt
    # tool hanging
    # tool error
    child_out_lines_num = 0
    expect_ret = aptget_proc.expect(expect_patterns)
    while expect_ret != EOF or expect_ret != TIMEOUT:
        line = "  " + aptget_proc.before
        if expect_ret == NL:
            click.echo(line)
        if expect_ret == INTERACT_PROMPT:
            click.echo(line, nl=False)
            aptget_proc.interact(escape_character="\r")
            aptget_proc.send("\n")

        # FIXME(azul) This should omit the reply sent by the user: y or n
        logger.info("apt-get output: {}".format(aptget_proc.before))
        child_out_lines_num += 1
        expect_ret = aptget_proc.expect(expect_patterns)
    aptget_proc.close()

    normal_termination = expect_ret == EOF and aptget_proc.exitstatus == 0

    return normal_termination


def dpkg_is_pkg_installed(pkg: str) -> bool:
    """Confirm whether pkg is installed using Debian's dpkg"""
    command_list = ["dpkg-query", "-f", "'${db:Status-Want}\n'", "-W", pkg]
    command = " ".join(command_list)
    output = pexpect.run(command, encoding="utf-8")

    install_match = re.search(r"install", output)
    if install_match:
        return True
    return False


# ****************** INSTALLERS ***********************************************


def ubuntu_install_zsh():
    """TODO"""

    if dpkg_is_pkg_installed("zsh"):
        click.echo("{} is already installed!".format("zsh"))
        logger.info("{} is already installed, skipping it".format("zsh"))
    else:
        click.echo("{} is not installed, would install it".format("zsh"))
        # install_success = aptget_install("zsh")


def ubuntu_install_programs():
    """TODO"""

    # Confirm root access privileges
    if os.geteuid() != 0:
        click.echo("This script requires root-level access. Please run it " +
                   "with sudo.")
        sys.exit(1)

    global logger
    global log_level
    logger = init_logger(log_level)
    logger.info("START: Starting instalation on Ubuntu")
    log_and_echo(logging.INFO, "Installing utilities...")

    # install_success = False
    # for pkg in aptget_packages:
    #     if dpkg_is_pkg_installed(pkg):
    #         click.echo("{} is already installed!".format(pkg))
    #         logger.info("{} is already installed, skipping it".format(pkg))
    #     else:
    #         click.echo("{} is not installed, would install it".format(pkg))
    #         # install_success = aptget_install(pkg)

    logger.info("FINISH: Finished installation.\n")
    click.echo("This installation script is a WIP")


# ****************** CLI DEFINITIONS ******************************************


@click.group()
def main():
    pass


@main.command()
@click.option(
    "-l",
    "--log-level",
    default="critical",
    show_default=True,
    help="Set the log level of the installer.",
    type=click.Choice(
        ["debug", "info", "warning", "error", "critical"],
        case_sensitive=False
    )
)
def ubuntu(arg_log_level):
    """Installs these dotfiles on Ubuntu-like distributions"""
    global log_level
    if arg_log_level == "debug":
        log_level = logging.DEBUG
    if arg_log_level == "info":
        log_level = logging.INFO
    elif arg_log_level == "warning":
        log_level = logging.WARNING
    elif arg_log_level == "error":
        log_level = logging.ERROR
    else:
        log_level = logging.CRITICAL

    ubuntu_install_programs()


if __name__ == "__main__":
    main()
