#!/usr/bin/env python3

import click
import os
from time import time_ns
from tempfile import mkdtemp


@click.command()
@click.argument("source", default=".", type=click.Path(dir_okay=False))
@click.argument("destination", default=".", type=click.Path())
def root_cmd(source: str, destination: str):
    """Unpack SOURCE T24 lib files, and store them in DESTINATION.

    \b
    SOURCE is a source lib or a directory containing libs.
    DESTINATION is the destination path to store the decompiled output.
    """
    click.echo(f"Unpacking T24 Libs from {source} to {destination}")

    # Review contents of JAR file
    # Extract API class files in case a decompiled version doesn't exist already
    # Decompile class files

    src_ext = os.path.splitext(source)[1]
    if src_ext != ".jar" and src_ext != ".class":
        raise click.BadArgumentUsage("SOURCE has to be a JAR or CLASS file.")

    tdir_abspath = mkdtemp(dir=".")

def unpack_jar():
    pass

def run_vineflower():
    pass


if __name__ == '__main__':
    root_cmd()
