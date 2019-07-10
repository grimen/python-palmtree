
# `palmtree` [![PyPI version](https://badge.fury.io/py/palmtree.svg)](https://badge.fury.io/py/palmtree) [![Build Status](https://travis-ci.com/grimen/python-palmtree.svg?token=sspjPRWbecBSpceU8Jyn&branch=master)](https://travis-ci.com/grimen/python-palmtree) [![Coverage Status](https://codecov.io/gh/grimen/python-palmtree/branch/master/graph/badge.svg)](https://codecov.io/gh/grimen/python-palmtree)

*A pretty filesystem tree inspection utility - for Python 3.*

![Screenshot](https://dvfr2lc5dhzsq.cloudfront.net/items/2C2w333H38250F1U3Z1i/Screen%20Shot%202019-03-08%20at%2016.15.29.png?X-CloudApp-Visitor-Id=675422)


## Introduction

TODO


## Install

Install using **pip**:

```sh
$ pip install palmtree
```


## Use

Very basic **[example](https://github.com/grimen/python-mybase/tree/master/examples/basic.py)**:

```python
import palmtree # NOTE: Python 3 is required

import os
import stat
import time
import datetime
import json
import colorful as color
import inspecta as util


# ==========================================================
#       EXAMPLE: log plain colorized output
# ----------------------------------------------------

print('[log/plain]: plain colorized output')

palmtree.log('./palmtree/tests/__fixtures__/foo')


# ==========================================================
#       EXAMPLE: log detailed custom colorized output
# -------------------------------------------------------

print('[log/detailed]: detailed custom colorized output')

def meta (item):
    try:
        item_stats = os.stat(item.resolved_path)

        item_byte_size = item_stats[stat.ST_SIZE]
        item_created_at_ms = item_stats[stat.ST_CTIME]
        item_created_at = time.strftime('%a %b %d %Y %H:%M:%S GMT%z (%Z)', time.localtime(item_created_at_ms))
        item_data = None

        if item.is_file:
            item_data = open(item.resolved_path, 'r').read()

        return ''.join([
            str(color.darkGray('- ')),
            ' '.join([
                str(color.white_on_darkMagenta(' {0} bytes '.format(item_byte_size))),
                str(item_data and json.dumps({'data': item_data}) or ''),
                str(color.darkCyan('{0}'.format(item_created_at))),
            ])
        ])

    except Exception as error:
        return color.yellow('(!) could not read/resolve')

palmtree.log('./palmtree/tests/__fixtures__/foo', meta = meta)


# ==========================================================
#       EXAMPLE: inspect plain output
# ----------------------------------------------------

print('[inspect/plain]: inspect plain colorized output')

inspection = palmtree.inspect('./palmtree/tests/__fixtures__/foo')

print('[inspect/plain]: {0}'.format(inspection))


# ==========================================================
#       EXAMPLE: inspect detailed custom output
# -------------------------------------------------------

print('[inspect/detailed]: inspect detailed custom colorized output')

inspection = palmtree.inspect('./palmtree/tests/__fixtures__/foo', meta = meta)

print('[inspect/detailed]:', inspection)


# ==========================================================
#       EXAMPLE: get plain object
# ----------------------------------------------------

print('[get/plain]: get plain object')

tree = palmtree.get('./palmtree/tests/__fixtures__/foo')

print('[get/plain]:', json.dumps(tree, indent = 4))


# ==========================================================
#       EXAMPLE: get detailed object
# -------------------------------------------------------

print('[get/plain]: get detailed object')

tree = palmtree.get('./palmtree/tests/__fixtures__/foo', meta = meta)

print('[get/plain]:', json.dumps(tree, indent = 4))

```

**Output:**

```sh
[log/plain]: plain colorized output

./palmtree/tests/__fixtures__/foo
├── bar
    ├── bar_1.txt
    ├── bar_2.txt
    └── baz
        ├── baz_1.txt
        └── baz_2.txt
├── baz  ⟶   ../bar/baz
├── baz_1.txt  ⟶   ../bar/baz/baz_1.txt
├── foo_1.txt
├── foo_2.txt
├── xxx  ⟶   ?
└── xxx.txt  ⟶   ?

[log/detailed]: detailed custom colorized output

./palmtree/tests/__fixtures__/foo
├── bar -  160 bytes   Thu Mar 07 2019 05:02:33 GMT-0500 (EST)
    ├── bar_1.txt -  6 bytes  {"data": "bar_1\n"} Thu Mar 07 2019 05:02:33 GMT-0500 (EST)
    ├── bar_2.txt -  6 bytes  {"data": "bar_2\n"} Thu Mar 07 2019 05:02:33 GMT-0500 (EST)
    └── baz -  128 bytes   Thu Mar 07 2019 05:02:33 GMT-0500 (EST)
        ├── baz_1.txt -  6 bytes  {"data": "baz_1\n"} Thu Mar 07 2019 05:02:33 GMT-0500 (EST)
        └── baz_2.txt -  6 bytes  {"data": "baz_2\n"} Thu Mar 07 2019 05:02:33 GMT-0500 (EST)
├── baz  ⟶   ../bar/baz -  128 bytes   Thu Mar 07 2019 05:02:33 GMT-0500 (EST)
├── baz_1.txt  ⟶   ../bar/baz/baz_1.txt -  6 bytes  {"data": "baz_1\n"} Thu Mar 07 2019 05:02:33 GMT-0500 (EST)
├── foo_1.txt -  6 bytes  {"data": "foo_1\n"} Thu Mar 07 2019 05:02:33 GMT-0500 (EST)
├── foo_2.txt -  6 bytes  {"data": "foo_2\n"} Thu Mar 07 2019 05:02:33 GMT-0500 (EST)
├── xxx  ⟶   ? (!) could not read/resolve
└── xxx.txt  ⟶   ? (!) could not read/resolve

[inspect/plain]: inspect plain colorized output
[inspect/plain]:
./palmtree/tests/__fixtures__/foo
├── bar
    ├── bar_1.txt
    ├── bar_2.txt
    └── baz
        ├── baz_1.txt
        └── baz_2.txt
├── baz  ⟶   ../bar/baz
├── baz_1.txt  ⟶   ../bar/baz/baz_1.txt
├── foo_1.txt
├── foo_2.txt
├── xxx  ⟶   ?
└── xxx.txt  ⟶   ?


[inspect/detailed]: inspect detailed custom colorized output
[inspect/detailed]:
./palmtree/tests/__fixtures__/foo
├── bar -  160 bytes   Thu Mar 07 2019 05:02:33 GMT-0500 (EST)
    ├── bar_1.txt -  6 bytes  {"data": "bar_1\n"} Thu Mar 07 2019 05:02:33 GMT-0500 (EST)
    ├── bar_2.txt -  6 bytes  {"data": "bar_2\n"} Thu Mar 07 2019 05:02:33 GMT-0500 (EST)
    └── baz -  128 bytes   Thu Mar 07 2019 05:02:33 GMT-0500 (EST)
        ├── baz_1.txt -  6 bytes  {"data": "baz_1\n"} Thu Mar 07 2019 05:02:33 GMT-0500 (EST)
        └── baz_2.txt -  6 bytes  {"data": "baz_2\n"} Thu Mar 07 2019 05:02:33 GMT-0500 (EST)
├── baz  ⟶   ../bar/baz -  128 bytes   Thu Mar 07 2019 05:02:33 GMT-0500 (EST)
├── baz_1.txt  ⟶   ../bar/baz/baz_1.txt -  6 bytes  {"data": "baz_1\n"} Thu Mar 07 2019 05:02:33 GMT-0500 (EST)
├── foo_1.txt -  6 bytes  {"data": "foo_1\n"} Thu Mar 07 2019 05:02:33 GMT-0500 (EST)
├── foo_2.txt -  6 bytes  {"data": "foo_2\n"} Thu Mar 07 2019 05:02:33 GMT-0500 (EST)
├── xxx  ⟶   ? (!) could not read/resolve
└── xxx.txt  ⟶   ? (!) could not read/resolve


[get/plain]: get plain object
[get/plain]: [
    {
        "level": 0,
        "path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/bar",
        "absolute_path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/bar",
        "relative_path": ".",
        "name": "bar",
        "extension": null,
        "key": "bar",
        "resolved_path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/bar",
        "resolved_absolute_path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/bar",
        "resolved_relative_path": ".",
        "resolved_name": "bar",
        "resolved_extension": null,
        "resolved_key": "bar",
        "is_resolved_directory": true,
        "is_resolved_file": false,
        "is_resolved_link": false,
        "is_directory": true,
        "is_file": false,
        "is_link": false,
        "is_resolved": true,
        "children": [
            {
                "level": 1,
                "path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/bar/bar_1.txt",
                "absolute_path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/bar/bar_1.txt",
                "relative_path": ".",
                "name": "bar_1.txt",
                "extension": ".txt",
                "key": "bar_1",
                "resolved_path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/bar/bar_1.txt",
                "resolved_absolute_path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/bar/bar_1.txt",
                "resolved_relative_path": ".",
                "resolved_name": "bar_1.txt",
                "resolved_extension": ".txt",
                "resolved_key": "bar_1",
                "is_resolved_directory": false,
                "is_resolved_file": true,
                "is_resolved_link": false,
                "is_directory": false,
                "is_file": true,
                "is_link": false,
                "is_resolved": true,
                "children": null,
                "meta": ""
            },
            {
                "level": 1,
                "path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/bar/bar_2.txt",
                "absolute_path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/bar/bar_2.txt",
                "relative_path": ".",
                "name": "bar_2.txt",
                "extension": ".txt",
                "key": "bar_2",
                "resolved_path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/bar/bar_2.txt",
                "resolved_absolute_path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/bar/bar_2.txt",
                "resolved_relative_path": ".",
                "resolved_name": "bar_2.txt",
                "resolved_extension": ".txt",
                "resolved_key": "bar_2",
                "is_resolved_directory": false,
                "is_resolved_file": true,
                "is_resolved_link": false,
                "is_directory": false,
                "is_file": true,
                "is_link": false,
                "is_resolved": true,
                "children": null,
                "meta": ""
            },
            {
                "level": 1,
                "path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/bar/baz",
                "absolute_path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/bar/baz",
                "relative_path": ".",
                "name": "baz",
                "extension": null,
                "key": "baz",
                "resolved_path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/bar/baz",
                "resolved_absolute_path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/bar/baz",
                "resolved_relative_path": ".",
                "resolved_name": "baz",
                "resolved_extension": null,
                "resolved_key": "baz",
                "is_resolved_directory": true,
                "is_resolved_file": false,
                "is_resolved_link": false,
                "is_directory": true,
                "is_file": false,
                "is_link": false,
                "is_resolved": true,
                "children": [
                    {
                        "level": 2,
                        "path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/bar/baz/baz_1.txt",
                        "absolute_path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/bar/baz/baz_1.txt",
                        "relative_path": ".",
                        "name": "baz_1.txt",
                        "extension": ".txt",
                        "key": "baz_1",
                        "resolved_path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/bar/baz/baz_1.txt",
                        "resolved_absolute_path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/bar/baz/baz_1.txt",
                        "resolved_relative_path": ".",
                        "resolved_name": "baz_1.txt",
                        "resolved_extension": ".txt",
                        "resolved_key": "baz_1",
                        "is_resolved_directory": false,
                        "is_resolved_file": true,
                        "is_resolved_link": false,
                        "is_directory": false,
                        "is_file": true,
                        "is_link": false,
                        "is_resolved": true,
                        "children": null,
                        "meta": ""
                    },
                    {
                        "level": 2,
                        "path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/bar/baz/baz_2.txt",
                        "absolute_path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/bar/baz/baz_2.txt",
                        "relative_path": ".",
                        "name": "baz_2.txt",
                        "extension": ".txt",
                        "key": "baz_2",
                        "resolved_path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/bar/baz/baz_2.txt",
                        "resolved_absolute_path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/bar/baz/baz_2.txt",
                        "resolved_relative_path": ".",
                        "resolved_name": "baz_2.txt",
                        "resolved_extension": ".txt",
                        "resolved_key": "baz_2",
                        "is_resolved_directory": false,
                        "is_resolved_file": true,
                        "is_resolved_link": false,
                        "is_directory": false,
                        "is_file": true,
                        "is_link": false,
                        "is_resolved": true,
                        "children": null,
                        "meta": ""
                    }
                ],
                "meta": ""
            }
        ],
        "meta": ""
    },
    {
        "level": 0,
        "path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/baz",
        "absolute_path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/baz",
        "relative_path": ".",
        "name": "baz",
        "extension": null,
        "key": "baz",
        "resolved_path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/bar/baz",
        "resolved_absolute_path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/bar/baz",
        "resolved_relative_path": "../bar/baz",
        "resolved_name": "baz",
        "resolved_extension": null,
        "resolved_key": "baz",
        "is_resolved_directory": true,
        "is_resolved_file": false,
        "is_resolved_link": false,
        "is_directory": true,
        "is_file": false,
        "is_link": true,
        "is_resolved": true,
        "children": null,
        "meta": ""
    },
    {
        "level": 0,
        "path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/baz_1.txt",
        "absolute_path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/baz_1.txt",
        "relative_path": ".",
        "name": "baz_1.txt",
        "extension": ".txt",
        "key": "baz_1",
        "resolved_path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/bar/baz/baz_1.txt",
        "resolved_absolute_path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/bar/baz/baz_1.txt",
        "resolved_relative_path": "../bar/baz/baz_1.txt",
        "resolved_name": "baz_1.txt",
        "resolved_extension": ".txt",
        "resolved_key": "baz_1",
        "is_resolved_directory": false,
        "is_resolved_file": true,
        "is_resolved_link": false,
        "is_directory": false,
        "is_file": true,
        "is_link": true,
        "is_resolved": true,
        "children": null,
        "meta": ""
    },
    {
        "level": 0,
        "path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/foo_1.txt",
        "absolute_path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/foo_1.txt",
        "relative_path": ".",
        "name": "foo_1.txt",
        "extension": ".txt",
        "key": "foo_1",
        "resolved_path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/foo_1.txt",
        "resolved_absolute_path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/foo_1.txt",
        "resolved_relative_path": ".",
        "resolved_name": "foo_1.txt",
        "resolved_extension": ".txt",
        "resolved_key": "foo_1",
        "is_resolved_directory": false,
        "is_resolved_file": true,
        "is_resolved_link": false,
        "is_directory": false,
        "is_file": true,
        "is_link": false,
        "is_resolved": true,
        "children": null,
        "meta": ""
    },
    {
        "level": 0,
        "path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/foo_2.txt",
        "absolute_path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/foo_2.txt",
        "relative_path": ".",
        "name": "foo_2.txt",
        "extension": ".txt",
        "key": "foo_2",
        "resolved_path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/foo_2.txt",
        "resolved_absolute_path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/foo_2.txt",
        "resolved_relative_path": ".",
        "resolved_name": "foo_2.txt",
        "resolved_extension": ".txt",
        "resolved_key": "foo_2",
        "is_resolved_directory": false,
        "is_resolved_file": true,
        "is_resolved_link": false,
        "is_directory": false,
        "is_file": true,
        "is_link": false,
        "is_resolved": true,
        "children": null,
        "meta": ""
    },
    {
        "level": 0,
        "path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/xxx",
        "absolute_path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/xxx",
        "relative_path": ".",
        "name": "xxx",
        "extension": null,
        "key": "xxx",
        "resolved_path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/xxx",
        "resolved_absolute_path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/xxx",
        "resolved_relative_path": ".",
        "resolved_name": "xxx",
        "resolved_extension": null,
        "resolved_key": "xxx",
        "is_resolved_directory": false,
        "is_resolved_file": false,
        "is_resolved_link": true,
        "is_directory": false,
        "is_file": false,
        "is_link": true,
        "is_resolved": false,
        "children": null,
        "meta": ""
    },
    {
        "level": 0,
        "path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/xxx.txt",
        "absolute_path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/xxx.txt",
        "relative_path": ".",
        "name": "xxx.txt",
        "extension": ".txt",
        "key": "xxx",
        "resolved_path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/xxx.txt",
        "resolved_absolute_path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/xxx.txt",
        "resolved_relative_path": ".",
        "resolved_name": "xxx.txt",
        "resolved_extension": ".txt",
        "resolved_key": "xxx",
        "is_resolved_directory": false,
        "is_resolved_file": false,
        "is_resolved_link": true,
        "is_directory": false,
        "is_file": false,
        "is_link": true,
        "is_resolved": false,
        "children": null,
        "meta": ""
    }
]
[get/plain]: get detailed object
[get/plain]: [
    {
        "level": 0,
        "path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/bar",
        "absolute_path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/bar",
        "relative_path": ".",
        "name": "bar",
        "extension": null,
        "key": "bar",
        "resolved_path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/bar",
        "resolved_absolute_path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/bar",
        "resolved_relative_path": ".",
        "resolved_name": "bar",
        "resolved_extension": null,
        "resolved_key": "bar",
        "is_resolved_directory": true,
        "is_resolved_file": false,
        "is_resolved_link": false,
        "is_directory": true,
        "is_file": false,
        "is_link": false,
        "is_resolved": true,
        "children": [
            {
                "level": 1,
                "path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/bar/bar_1.txt",
                "absolute_path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/bar/bar_1.txt",
                "relative_path": ".",
                "name": "bar_1.txt",
                "extension": ".txt",
                "key": "bar_1",
                "resolved_path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/bar/bar_1.txt",
                "resolved_absolute_path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/bar/bar_1.txt",
                "resolved_relative_path": ".",
                "resolved_name": "bar_1.txt",
                "resolved_extension": ".txt",
                "resolved_key": "bar_1",
                "is_resolved_directory": false,
                "is_resolved_file": true,
                "is_resolved_link": false,
                "is_directory": false,
                "is_file": true,
                "is_link": false,
                "is_resolved": true,
                "children": null,
                "meta": "\u001b[38;5;248m- \u001b[39m\u001b[38;5;231m\u001b[48;5;127m 6 bytes \u001b[39m\u001b[49m {\"data\": \"bar_1\\n\"} \u001b[38;5;37mThu Mar 07 2019 05:02:33 GMT-0500 (EST)\u001b[39m"
            },
            {
                "level": 1,
                "path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/bar/bar_2.txt",
                "absolute_path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/bar/bar_2.txt",
                "relative_path": ".",
                "name": "bar_2.txt",
                "extension": ".txt",
                "key": "bar_2",
                "resolved_path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/bar/bar_2.txt",
                "resolved_absolute_path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/bar/bar_2.txt",
                "resolved_relative_path": ".",
                "resolved_name": "bar_2.txt",
                "resolved_extension": ".txt",
                "resolved_key": "bar_2",
                "is_resolved_directory": false,
                "is_resolved_file": true,
                "is_resolved_link": false,
                "is_directory": false,
                "is_file": true,
                "is_link": false,
                "is_resolved": true,
                "children": null,
                "meta": "\u001b[38;5;248m- \u001b[39m\u001b[38;5;231m\u001b[48;5;127m 6 bytes \u001b[39m\u001b[49m {\"data\": \"bar_2\\n\"} \u001b[38;5;37mThu Mar 07 2019 05:02:33 GMT-0500 (EST)\u001b[39m"
            },
            {
                "level": 1,
                "path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/bar/baz",
                "absolute_path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/bar/baz",
                "relative_path": ".",
                "name": "baz",
                "extension": null,
                "key": "baz",
                "resolved_path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/bar/baz",
                "resolved_absolute_path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/bar/baz",
                "resolved_relative_path": ".",
                "resolved_name": "baz",
                "resolved_extension": null,
                "resolved_key": "baz",
                "is_resolved_directory": true,
                "is_resolved_file": false,
                "is_resolved_link": false,
                "is_directory": true,
                "is_file": false,
                "is_link": false,
                "is_resolved": true,
                "children": [
                    {
                        "level": 2,
                        "path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/bar/baz/baz_1.txt",
                        "absolute_path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/bar/baz/baz_1.txt",
                        "relative_path": ".",
                        "name": "baz_1.txt",
                        "extension": ".txt",
                        "key": "baz_1",
                        "resolved_path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/bar/baz/baz_1.txt",
                        "resolved_absolute_path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/bar/baz/baz_1.txt",
                        "resolved_relative_path": ".",
                        "resolved_name": "baz_1.txt",
                        "resolved_extension": ".txt",
                        "resolved_key": "baz_1",
                        "is_resolved_directory": false,
                        "is_resolved_file": true,
                        "is_resolved_link": false,
                        "is_directory": false,
                        "is_file": true,
                        "is_link": false,
                        "is_resolved": true,
                        "children": null,
                        "meta": "\u001b[38;5;248m- \u001b[39m\u001b[38;5;231m\u001b[48;5;127m 6 bytes \u001b[39m\u001b[49m {\"data\": \"baz_1\\n\"} \u001b[38;5;37mThu Mar 07 2019 05:02:33 GMT-0500 (EST)\u001b[39m"
                    },
                    {
                        "level": 2,
                        "path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/bar/baz/baz_2.txt",
                        "absolute_path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/bar/baz/baz_2.txt",
                        "relative_path": ".",
                        "name": "baz_2.txt",
                        "extension": ".txt",
                        "key": "baz_2",
                        "resolved_path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/bar/baz/baz_2.txt",
                        "resolved_absolute_path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/bar/baz/baz_2.txt",
                        "resolved_relative_path": ".",
                        "resolved_name": "baz_2.txt",
                        "resolved_extension": ".txt",
                        "resolved_key": "baz_2",
                        "is_resolved_directory": false,
                        "is_resolved_file": true,
                        "is_resolved_link": false,
                        "is_directory": false,
                        "is_file": true,
                        "is_link": false,
                        "is_resolved": true,
                        "children": null,
                        "meta": "\u001b[38;5;248m- \u001b[39m\u001b[38;5;231m\u001b[48;5;127m 6 bytes \u001b[39m\u001b[49m {\"data\": \"baz_2\\n\"} \u001b[38;5;37mThu Mar 07 2019 05:02:33 GMT-0500 (EST)\u001b[39m"
                    }
                ],
                "meta": "\u001b[38;5;248m- \u001b[39m\u001b[38;5;231m\u001b[48;5;127m 128 bytes \u001b[39m\u001b[49m  \u001b[38;5;37mThu Mar 07 2019 05:02:33 GMT-0500 (EST)\u001b[39m"
            }
        ],
        "meta": "\u001b[38;5;248m- \u001b[39m\u001b[38;5;231m\u001b[48;5;127m 160 bytes \u001b[39m\u001b[49m  \u001b[38;5;37mThu Mar 07 2019 05:02:33 GMT-0500 (EST)\u001b[39m"
    },
    {
        "level": 0,
        "path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/baz",
        "absolute_path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/baz",
        "relative_path": ".",
        "name": "baz",
        "extension": null,
        "key": "baz",
        "resolved_path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/bar/baz",
        "resolved_absolute_path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/bar/baz",
        "resolved_relative_path": "../bar/baz",
        "resolved_name": "baz",
        "resolved_extension": null,
        "resolved_key": "baz",
        "is_resolved_directory": true,
        "is_resolved_file": false,
        "is_resolved_link": false,
        "is_directory": true,
        "is_file": false,
        "is_link": true,
        "is_resolved": true,
        "children": null,
        "meta": "\u001b[38;5;248m- \u001b[39m\u001b[38;5;231m\u001b[48;5;127m 128 bytes \u001b[39m\u001b[49m  \u001b[38;5;37mThu Mar 07 2019 05:02:33 GMT-0500 (EST)\u001b[39m"
    },
    {
        "level": 0,
        "path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/baz_1.txt",
        "absolute_path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/baz_1.txt",
        "relative_path": ".",
        "name": "baz_1.txt",
        "extension": ".txt",
        "key": "baz_1",
        "resolved_path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/bar/baz/baz_1.txt",
        "resolved_absolute_path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/bar/baz/baz_1.txt",
        "resolved_relative_path": "../bar/baz/baz_1.txt",
        "resolved_name": "baz_1.txt",
        "resolved_extension": ".txt",
        "resolved_key": "baz_1",
        "is_resolved_directory": false,
        "is_resolved_file": true,
        "is_resolved_link": false,
        "is_directory": false,
        "is_file": true,
        "is_link": true,
        "is_resolved": true,
        "children": null,
        "meta": "\u001b[38;5;248m- \u001b[39m\u001b[38;5;231m\u001b[48;5;127m 6 bytes \u001b[39m\u001b[49m {\"data\": \"baz_1\\n\"} \u001b[38;5;37mThu Mar 07 2019 05:02:33 GMT-0500 (EST)\u001b[39m"
    },
    {
        "level": 0,
        "path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/foo_1.txt",
        "absolute_path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/foo_1.txt",
        "relative_path": ".",
        "name": "foo_1.txt",
        "extension": ".txt",
        "key": "foo_1",
        "resolved_path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/foo_1.txt",
        "resolved_absolute_path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/foo_1.txt",
        "resolved_relative_path": ".",
        "resolved_name": "foo_1.txt",
        "resolved_extension": ".txt",
        "resolved_key": "foo_1",
        "is_resolved_directory": false,
        "is_resolved_file": true,
        "is_resolved_link": false,
        "is_directory": false,
        "is_file": true,
        "is_link": false,
        "is_resolved": true,
        "children": null,
        "meta": "\u001b[38;5;248m- \u001b[39m\u001b[38;5;231m\u001b[48;5;127m 6 bytes \u001b[39m\u001b[49m {\"data\": \"foo_1\\n\"} \u001b[38;5;37mThu Mar 07 2019 05:02:33 GMT-0500 (EST)\u001b[39m"
    },
    {
        "level": 0,
        "path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/foo_2.txt",
        "absolute_path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/foo_2.txt",
        "relative_path": ".",
        "name": "foo_2.txt",
        "extension": ".txt",
        "key": "foo_2",
        "resolved_path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/foo_2.txt",
        "resolved_absolute_path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/foo_2.txt",
        "resolved_relative_path": ".",
        "resolved_name": "foo_2.txt",
        "resolved_extension": ".txt",
        "resolved_key": "foo_2",
        "is_resolved_directory": false,
        "is_resolved_file": true,
        "is_resolved_link": false,
        "is_directory": false,
        "is_file": true,
        "is_link": false,
        "is_resolved": true,
        "children": null,
        "meta": "\u001b[38;5;248m- \u001b[39m\u001b[38;5;231m\u001b[48;5;127m 6 bytes \u001b[39m\u001b[49m {\"data\": \"foo_2\\n\"} \u001b[38;5;37mThu Mar 07 2019 05:02:33 GMT-0500 (EST)\u001b[39m"
    },
    {
        "level": 0,
        "path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/xxx",
        "absolute_path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/xxx",
        "relative_path": ".",
        "name": "xxx",
        "extension": null,
        "key": "xxx",
        "resolved_path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/xxx",
        "resolved_absolute_path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/xxx",
        "resolved_relative_path": ".",
        "resolved_name": "xxx",
        "resolved_extension": null,
        "resolved_key": "xxx",
        "is_resolved_directory": false,
        "is_resolved_file": false,
        "is_resolved_link": true,
        "is_directory": false,
        "is_file": false,
        "is_link": true,
        "is_resolved": false,
        "children": null,
        "meta": "\u001b[38;5;226m(!) could not read/resolve\u001b[39m"
    },
    {
        "level": 0,
        "path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/xxx.txt",
        "absolute_path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/xxx.txt",
        "relative_path": ".",
        "name": "xxx.txt",
        "extension": ".txt",
        "key": "xxx",
        "resolved_path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/xxx.txt",
        "resolved_absolute_path": "/Users/grimen/Dev/Private/python-palmtree/palmtree/tests/__fixtures__/foo/xxx.txt",
        "resolved_relative_path": ".",
        "resolved_name": "xxx.txt",
        "resolved_extension": ".txt",
        "resolved_key": "xxx",
        "is_resolved_directory": false,
        "is_resolved_file": false,
        "is_resolved_link": true,
        "is_directory": false,
        "is_file": false,
        "is_link": true,
        "is_resolved": false,
        "children": null,
        "meta": "\u001b[38;5;226m(!) could not read/resolve\u001b[39m"
    }
]
```


## Test

Clone down source code:

```sh
$ make install
```

Run **colorful tests**, with only native environment (dependency sandboxing up to you):

```sh
$ make test
```

Run **less colorful tests**, with **multi-environment** (using **tox**):

```sh
$ make test-tox
```


## Related

- [**`node-palmtree`**](https://github.com/grimen/node-palmtree) - *"A pretty filesystem tree inspection utility - for Node.js"*


## About

This project was mainly initiated - in lack of solid existing alternatives - to be used at our work at **[Markable.ai](https://markable.ai)** to have common code conventions between various programming environments where **Python** (research, CV, AI) is heavily used.


## License

Released under the MIT license.
