#!/usr/bin/env python3

import click
import os
import zipfile
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
    if src_ext != ".jar":
        raise click.BadArgumentUsage("SOURCE has to be a JAR")

    tdir_abspath = mkdtemp(dir=".")

    with zipfile.ZipFile(source, mode="r") as jarfile:
        jar_namelist = jarfile.namelist()
        for name in jar_namelist:
            valid_jar = is_valid_jar_member(name, jar_namelist)
            click.echo(f"Should {name} be extracted: {valid_jar}")
            if valid_jar:
                jarfile.extract(name, tdir_abspath)


def is_valid_jar_member(target_member: str, jar_members: list[str]) -> bool:
    """Determine if a jar member is valid, and should be extracted."""
    target_root, target_ext = os.path.splitext(target_member)
    has_class_ext = target_ext == ".class"
    has_java_ext = target_ext == ".java"
    is_cl_class_member = target_member.endswith("_cl.class")

    java_equiv_exists = False
    if has_class_ext:
        java_equiv_name = target_root + ".java"
        java_equiv_exists = java_equiv_name in jar_members

    is_valid = (
        has_java_ext or (
            not is_cl_class_member and
            has_class_ext and
            not java_equiv_exists
        )
    )

    return is_valid


if __name__ == '__main__':
    root_cmd()
