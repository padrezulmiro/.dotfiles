#!/usr/bin/env python3

import click
import os
import glob
import math
from tempfile import mkdtemp
import subprocess
import tempfile

class JarList:
    """"""

    def __init__(self):
        """Create a new JarList instance."""
        self._list = []
        self._len = 0

    def __len__(self):
        """Length of this JarList."""
        return len(self._list)

    def append(self, el: str):
        """Append EL to this JarList."""
        self._list.append(el)
        self._len += len(el)

    def char_length(self):
        """Return the sum character length across this JarList."""
        return self._len


class PartitionedList:
    """"""

    def __init__(self, partitions=1, max_length=100000):
        """Init new PartitionedList."""
        self._max_jarlist_length = max_length
        self._partition_index = 0
        self._partitions: list[JarList] = []
        for i in range(partitions):
            self._partitions.append(JarList())

    def append(self, el: str):
        """Append EL to this PartitionSet."""
        current_length = self._partitions[self._partition_index].char_length()
        updated_length = current_length + len(el)

        # TODO branch over ARG_MAX, creating a new partition if needed
        if updated_length < self._max_jarlist_length:
            self._partitions[self._partition_index].append(el)
        else:
            # TODO
            # Create a new partition
            # Append el to new partition
            # Reflow the partitions' elements to maintain balance
            total_el_number = 0
            for partition in self._partitions:
                total_el_number += len(partition)
            new_partition = JarList()
            self._partitions.append(JarList())
            pass



@click.command()
@click.argument("source", default=".", type=click.Path(dir_okay=True))
@click.argument("destination", default=".", type=click.Path())
@click.option("-p", "--procs", "nprocs", default=1, type=click.IntRange(1, 4))
def root_cmd(source: str, destination: str, nprocs: int):
    r"""
    Unpack SOURCE T24 lib files, and store them in DESTINATION.

    \b
    SOURCE is a source lib or a directory containing libs.
    DESTINATION is the destination path to store the decompiled output.
    """
    click.echo(f"Unpacking T24 Libs from {source} to {destination}")

    # TODO validate inputs
    # src_ext = os.path.splitext(source)[1]
    # if src_ext != ".jar":
    #     raise click.BadArgumentUsage("SOURCE has to be a JAR")

    if os.path.isdir(source):
        breakpoint()
        jars = list_jars(source)
        partitions = partition_jars(jars, nprocs)
        # parallel_unpack_jars(partitions)
    else:
        # TODO
        pass


def list_jars(source: str) -> list[str]:
    """
    List eligible target jars in SOURCE to unpack.
    """
    srcdir_els = glob.glob("**/*.jar", root_dir=source, recursive=True)

    seen = set()
    unique_srcdir_els = []
    for el in srcdir_els:
        _, basename = os.path.split(el)
        if basename not in seen:
            seen.add(basename)
            unique_srcdir_els.append(el)

    return unique_srcdir_els


def partition_jars(targets: list[str], partition_num: int) -> list[list[str]]:
    """
    Partition TARGETS into PARTITION_NUM chunks.

    The algorithm creates a minimum of PARTITION_NUM chunks unless one
    partition would have more than the equivalent of 100KB of characters
    inside. This is to avoid running into issues with the system's ARG_MAX
    limit.

    Therefore, this function will create as many partitions as necessary to
    disallow that from happening.
    """
    MAX_LENGTH = 100000

    targets_size = len(targets)
    partition_size = math.ceil(targets_size / partition_num)

    partitions = []
    for i in range(0, targets_size, partition_size):
        slice_start = i
        slice_end = (targets_size if
                     i + partition_size > targets_size else
                     i + partition_size)
        targets_slice = targets[slice_start:slice_end]

        targets_slice_length = 0
        for target in targets_slice:
            targets_slice_length += len(target)

        partitions.append(targets[slice_start:slice_end])

    return partitions


def unpack_jars(targets: list[list[str]]) -> None:
    """Unpack jar archives in TARGETS."""
    temp_root_dir = tempfile.mkdtemp(prefix="unpck-")
    temp_dirs_list: list[str] = []

    MAXIMUM_PROCS: int = 4
    proc_list: list[subprocess.Popen] = []

    for target in targets:
        temp_dirs_list.append(tempfile.mkdtemp(dir=temp_root_dir))

        # Run vineflower pointing to that temp dir
        # proc_list.append(run_vineflower())

        #
        pass
    pass


def extract_jar(jar: str, temp_dir: str):
    """Extract JAR valid contents to TEMP_DIR."""
    jar_namelist = jar.namelist()
    for name in jar_namelist:
        valid_jar = is_valid_jar_member(name, jar_namelist)
        if valid_jar:
            jar.extract(name, temp_dir)


def is_valid_jar_member(target_member: str, jar_members: list[str]) -> bool:
    """
    Determine if a jar content file should extracted.

    The criteria are whether
    """
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


def run_vineflower(jars: list[str]) -> subprocess.Popen:
    click.echo(f"Run 'vineflower'")


if __name__ == '__main__':
    root_cmd()
