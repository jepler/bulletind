<!--
SPDX-FileCopyrightText: 2021 Jeff Epler

SPDX-License-Identifier: GPL-3.0-only
-->
[![Test bulletind](https://github.com/jepler/bulletind/actions/workflows/test.yml/badge.svg)](https://github.com/jepler/bulletind/actions/workflows/test.yml)
[![Update Bulletin D data](https://github.com/jepler/bulletind/actions/workflows/cron.yml/badge.svg)](https://github.com/jepler/bulletind/actions/workflows/cron.yml)
[![PyPI](https://img.shields.io/pypi/v/bulletind)](https://pypi.org/project/bulletind)
![Lines of code](https://img.shields.io/tokei/lines/github/jepler/bulletind)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/jepler/bulletind.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/jepler/bulletind/context:python)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/jepler/bulletind/main.svg)](https://results.pre-commit.ci/latest/github/jepler/bulletind/main)


# Purpose

bulletind provides access to the IERS "Bulletin D" data to Python or to other
software that can process JSON data.

"Bulletin D" is the publication that specifies the "DUT1 offset", the
difference between UTC and UT1, in units of 0.1 seconds. This is the value that
is ostensibly transmitted on various broadcast time signals, such as WWVB.

The source of the data is
https://datacenter.iers.org/availableVersions.php?id=17 and covers April 1991
through the present. (the oldest Bulletin available is Number 21 issued
1991-04-22)


# Use

bulletind includes bulletin data that was available the last time the software
was updated. Further updates can be downloaded to a per-user cache with
the `bulletind update` command or the `get_bulletin_d_data()` function.
Cached data can be printed as json with `bulletind json`, as tabular data with
`bulletind table`, or accessed with the `get_cached_bulletin_d_data()` function.

The structure of the data is described by the `BulletinDInfo` type.
In json and tabular formats, dates are represented in the ISO standard format
YYYY-mm-dd.


# Development status

The author (@jepler) occasionally develops and maintains this project, but
issues are not likely to be acted on.  They would be interested in adding
co-maintainer(s).
