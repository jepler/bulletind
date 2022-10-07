#!/usr/bin/python3
# Copyright (C) 2022 Jeff Epler <jepler@gmail.com>
# SPDX-FileCopyrightText: 2022 Jeff Epler
#
# SPDX-License-Identifier: GPL-3.0-only

"""Commandline interface to 'Bulletin D' data"""
import json as json_
import pathlib

import click

from . import BulletinDInfo, get_bulletin_d_data, get_cached_bulletin_d_data


@click.group()
def cli() -> None:
    """Download and show Bulletin D data in json format"""


@cli.command()
@click.option(
    "--update-package-data/--no-update-package-data",
    default=False,
    help="Update package data, not user cache",
)
def update(update_package_data: bool) -> None:
    """Update data from IERS"""
    if update_package_data:
        get_bulletin_d_data([pathlib.Path(__file__).resolve().parent / "data"])
    else:
        get_bulletin_d_data()


@cli.command()
def json() -> None:
    """Print all data in JSON format"""
    data = get_cached_bulletin_d_data()
    data = sorted(data, key=lambda x: x.number)
    json_data = BulletinDInfo.schema().dump(data, many=True)
    print(json_.dumps(json_data, indent=4))


@cli.command()
def table() -> None:
    "Print all data in tabular format"
    data = get_cached_bulletin_d_data()
    data = sorted(data, key=lambda x: x.number)
    end = None
    for start, end in zip(data, data[1:]):
        daycount = (end.start_date - start.start_date).days
        opt_ls = "LS" if (start.dut1 * end.dut1 < 0) else "  "
        print(
            f"{start.start_date} {start.dut1: 4.1f} {daycount:4} {opt_ls} "
            f"# Bulletin {start.number:4} issued {start.date}, "
            f"{(start.start_date - start.date).days} early"
        )
    if end is not None:
        print(f"{end.start_date} {end.dut1: 4.1f}")


if __name__ == "__main__":
    cli()
