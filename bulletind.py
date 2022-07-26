#!/usr/bin/python3
"""Retrieve 'bulletin D' data"""

import json
import os
import pathlib
import sys
import typing
import xml.etree.ElementTree

import bs4
import click
import platformdirs
import requests

# Copyright (C) 2011-2020 Jeff Epler <jepler@gmail.com>
# SPDX-FileCopyrightText: 2022 Jeff Epler
#
# SPDX-License-Identifier: GPL-3.0-only

BULLETIN_D_INDEX = "https://datacenter.iers.org/availableVersions.php?id=17"

DATA_PATHS = [
    platformdirs.user_cache_path(appname="wwvbpy"),
    pathlib.Path(__file__).resolve().parent / "data",
]


KEYS = [
    ("date", str),
    ("startDate", str),
    ("DUT1", float),
    ("startUTC", float),
]


class BulletinDInfo(typing.TypedDict):
    """Type representing a Bulletin D dictionary"""

    date: str
    startdate: str
    dut1: float
    dut1_unit: str
    startutc: float


def cache(
    url: str, cache_paths: typing.Optional[list[pathlib.Path]] = None
) -> BulletinDInfo:
    """Download a specific Bulletin & cache it in json format"""
    base = url.split("/")[-1].split(".")[0]

    cache_paths = cache_paths or DATA_PATHS
    for path in cache_paths:
        loc = path / f"{base}.json"
        if loc.exists():
            with open(loc, "r", encoding="utf-8") as data_file:
                return typing.cast(BulletinDInfo, json.load(data_file))

    loc = cache_paths[0] / f"{base}.json"
    tmp_loc = cache_paths[0] / f"{base}.json.tmp"

    print(f"Fetching {url} to {loc}", file=sys.stderr)
    buld_xml = requests.get(url).text
    doc = xml.etree.ElementTree.XML(buld_xml)
    data = {}
    for element_name, transformer in KEYS:
        element = doc.find(f".//{{http://www.iers.org/2003/schema/iers}}{element_name}")
        assert element is not None
        data[element_name.lower()] = transformer(element.text)

    element = doc.find(".//{http://www.iers.org/2003/schema/iers}DUT1")
    assert element is not None
    data["dut1_unit"] = element.attrib.get("unit", "s")

    with open(tmp_loc, "wt", encoding="utf-8") as data_file:
        print(json.dumps(data), file=data_file)
        data_file.close()
        os.rename(tmp_loc, loc)
        print(data)
        return typing.cast(BulletinDInfo, data)


def get_bulletin_d_data(
    cache_paths: typing.Optional[list[pathlib.Path]] = None,
) -> list[BulletinDInfo]:
    """Download and return all available Bulletin D data"""
    for path in DATA_PATHS:
        os.makedirs(path, exist_ok=True)

    buld_text = requests.get(BULLETIN_D_INDEX).text
    buld_data = bs4.BeautifulSoup(buld_text, features="html.parser")
    refs = buld_data.findAll(lambda tag: "xml" in tag.get("href", ""))

    return [cache(r["href"], cache_paths) for r in refs]


def get_cached_bulletin_d_data() -> list[BulletinDInfo]:
    """Return all cached Bulletin D data"""

    def content(filename: pathlib.Path) -> BulletinDInfo:
        with open(filename, "r", encoding="utf-8") as data_file:
            return typing.cast(BulletinDInfo, json.load(data_file))

    return [content(p) for path in DATA_PATHS for p in path.glob("*.json")]


@click.command()
@click.option(
    "--cache-only/--no-cache-only",
    default=False,
    help="Only retrieve cached data files",
)
@click.option(
    "--update-package-data/--no-update-package-data",
    default=False,
    help="Update package data, not user cache",
)
def main(cache_only: bool, update_package_data: bool) -> None:
    """Download and show Bulletin D data in json format"""
    if update_package_data:
        get_bulletin_d_data([pathlib.Path(__file__).resolve().parent / "data"])
    else:
        if cache_only:
            data = get_cached_bulletin_d_data()
        else:
            data = get_bulletin_d_data()
        data = sorted(data, key=lambda x: typing.cast(float, x.get("number", 0)))
        json.dump(data, indent=4, fp=sys.stdout)
        print()


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
