#!/usr/bin/env python3

import click


@click.command()
@click.argument("source", default=".", type=click.Path())
@click.argument("destination", default=".", type=click.Path())
def unpack(source: str, destination: str):
    """
    Unpack SOURCE T24 lib files, and store them in DESTINATION.

    SOURCE is a source lib or a directory containing libs.
    DESTINATION is the destination path to store the decompiled output.
    """
    click.echo(source)
    click.echo(destination)
    pass


def unzip_files():
    pass


def del_extra_class_files():
    pass

def run_vineflower():
    pass

if __name__ == '__main__':
    unpack()
