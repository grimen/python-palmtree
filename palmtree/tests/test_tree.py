
# coding: utf-8

# =========================================
#       IMPORTS
# --------------------------------------

import rootpath

rootpath.append()

from palmtree.tests import helper

import palmtree

import os
import stat
import time
import re
import json
import inspecta
import warnings

from os import path
from os import environ as env
from six import string_types
import colorful as color

from attributedict.collections import AttributeDict


# =========================================
#       CONFIG
# --------------------------------------

warnings.simplefilter(action = 'ignore', category = FutureWarning)


# =========================================
#       HELPERS
# --------------------------------------

def require(filepath):
    filepath = path.abspath(filepath)

    data = None

    with open(filepath) as file:
        data = file.read()

    data = data and json.loads(data)

    return data

# @see: https://github.com/chalk/ansi-regex
def strip_ansi(value):
    pattern = '|'.join([
        '[\\u001B\\u009B][[\\]()#;?]*(?:(?:(?:[a-zA-Z\\d]*(?:;[-a-zA-Z\\d\\/#&.:=?%@~_]*)*)?\\u0007)',
        '(?:(?:\\d{1,4}(?:;\\d{0,4})*)?[\\dA-PR-TZcf-ntqry=><~]))'
    ])

    pattern_regexp = re.compile(pattern, re.M | re.I)

    return re.sub(pattern_regexp, '', value)

def resolve_fixture_data_paths(data):
    if isinstance(data, list):
        return list(map(resolve_fixture_data_paths, data))

    if isinstance(data, dict):
        mapped_object = dict(data)

        ENV_VARIABLE_PATTERN = '\\$([a-zA-Z_][a-zA-Z0-9_]+)'

        for key, value in data.items():
            if value:
                if isinstance(value, string_types):
                    value = re.compile(ENV_VARIABLE_PATTERN).sub(lambda match: (
                        env.get(match.group(1)) or '${0}'.format(match.group(1))
                    ), value)

                elif isinstance(value, list):
                    value = list(map(resolve_fixture_data_paths, value))

                elif isinstance(value, dict):
                    value = resolve_fixture_data_paths(value)

            mapped_object[key] = value

        return mapped_object

    return data

def map_fixture_tree_meta_fields(data, map_key, mapper):
    if isinstance(data, list):
        return list(map(lambda data: (
            map_fixture_tree_meta_fields(data, map_key, mapper)
        ), data))

    if isinstance(data, dict):
        mapped_object = dict(data)

        for key, value in data.items():
            if key == map_key:
                try:
                    value = mapper(data)

                except Exception as error:
                    pass

            if isinstance(value, list):
                value = list(map(lambda value: (
                    map_fixture_tree_meta_fields(value, map_key, mapper)
                ), value))

            elif isinstance(value, dict):
                value = map_fixture_tree_meta_fields(value, mapKey, mapper)

            mapped_object[key] = value

        return mapped_object

    return data

def cast_dicts(value):
    if isinstance(value, tuple):
        return tuple(cast_dicts(list(value)))

    elif isinstance(value, list):
        return list(map(cast_dicts, value))

    elif isinstance(value, dict):
        return dict(AttributeDict.dict(value))

    return value

# =========================================
#       FIXTURES
# --------------------------------------

FOO_GET_OBJECT = resolve_fixture_data_paths(require('./palmtree/tests/__fixtures__/get_foo.json'))

VALID_FOLDER_PATH = path.abspath('./palmtree/tests/__fixtures__/foo')
VALID_FILE_PATH = path.abspath('./palmtree/tests/__fixtures__/foo/foo_1.txt')

INVALID_FOLDER_PATH = path.abspath('./palmtree/tests/__fixtures__/xxx')
INVALID_FILE_PATH = path.abspath('./palmtree/tests/__fixtures__/xxx/foo_1.txt')


# =========================================
#       TEST
# --------------------------------------

class TestCase(helper.TestCase):

    def test__import(self):
        self.assertModule(palmtree)

    def test_get(self):
        self.assertTrue(hasattr(palmtree, 'get'))
        self.assertTrue(callable(palmtree.get))

        def meta(item):
            try:
                data = None

                with open(item.get('resolved_path')) as file:
                    data = file.read().strip()

                return data

            except Exception as error:
                return ''

        MAPPED_FOO_GET_OBJECT = map_fixture_tree_meta_fields(FOO_GET_OBJECT, 'meta', meta)

        # ---

        self.assertEqual(cast_dicts(palmtree.get(VALID_FOLDER_PATH)), FOO_GET_OBJECT)

        with self.assertRaises(palmtree.Error):
            palmtree.get(VALID_FILE_PATH)

        with self.assertRaises(palmtree.Error):
            palmtree.get(INVALID_FOLDER_PATH)

        with self.assertRaises(palmtree.Error):
            palmtree.get(INVALID_FILE_PATH)

        # ---

        self.assertEqual(cast_dicts(palmtree.get(VALID_FOLDER_PATH, silent = True)), FOO_GET_OBJECT)
        self.assertEqual(cast_dicts(palmtree.get(VALID_FILE_PATH, silent = True)), [])
        self.assertEqual(cast_dicts(palmtree.get(INVALID_FOLDER_PATH, silent = True)), [])
        self.assertEqual(cast_dicts(palmtree.get(INVALID_FILE_PATH, silent = True)), [])

        # ---

        self.assertEqual(palmtree.get(VALID_FOLDER_PATH, meta = meta), MAPPED_FOO_GET_OBJECT)

        with self.assertRaises(palmtree.Error):
            palmtree.get(VALID_FILE_PATH, meta = meta)

        with self.assertRaises(palmtree.Error):
            palmtree.get(INVALID_FOLDER_PATH, meta = meta)

        with self.assertRaises(palmtree.Error):
            palmtree.get(INVALID_FILE_PATH, meta = meta)

        # ---

        self.assertEqual(cast_dicts(palmtree.get(VALID_FOLDER_PATH, meta = meta, silent = True)), MAPPED_FOO_GET_OBJECT)
        self.assertEqual(cast_dicts(palmtree.get(VALID_FILE_PATH, meta = meta, silent = True)), [])
        self.assertEqual(cast_dicts(palmtree.get(INVALID_FOLDER_PATH, meta = meta, silent = True)), [])
        self.assertEqual(cast_dicts(palmtree.get(INVALID_FILE_PATH, meta = meta, silent = True)), [])

    def test_inspect(self):
        self.assertTrue(hasattr(palmtree, 'inspect'))
        self.assertTrue(callable(palmtree.inspect))

        result = None

        # ---

        result = palmtree.inspect(VALID_FOLDER_PATH)

        self.assertEqual(strip_ansi(result), strip_ansi('\n{PWD}/palmtree/tests/__fixtures__/foo\n├── bar \n    ├── bar_1.txt \n    ├── bar_2.txt \n    └── baz \n        ├── baz_1.txt \n        └── baz_2.txt \n├── baz  ⟶   ../bar/baz \n├── baz_1.txt  ⟶   ../bar/baz/baz_1.txt \n├── foo_1.txt \n├── foo_2.txt \n├── xxx  ⟶   ? \n└── xxx.txt  ⟶   ? \n\n'.format(PWD = env.get('PWD'))))

        with self.assertRaises(palmtree.Error):
            palmtree.get(VALID_FILE_PATH)

        with self.assertRaises(palmtree.Error):
            palmtree.get(INVALID_FOLDER_PATH)

        with self.assertRaises(palmtree.Error):
            palmtree.get(INVALID_FILE_PATH)

        # ---

        result = palmtree.inspect(VALID_FOLDER_PATH, silent = True)

        self.assertEqual(strip_ansi(result), strip_ansi('\n{PWD}/palmtree/tests/__fixtures__/foo\n├── bar \n    ├── bar_1.txt \n    ├── bar_2.txt \n    └── baz \n        ├── baz_1.txt \n        └── baz_2.txt \n├── baz  ⟶   ../bar/baz \n├── baz_1.txt  ⟶   ../bar/baz/baz_1.txt \n├── foo_1.txt \n├── foo_2.txt \n├── xxx  ⟶   ? \n└── xxx.txt  ⟶   ? \n\n'.format(PWD = env.get('PWD'))))

        result = palmtree.inspect(VALID_FILE_PATH, silent = True)

        self.assertEqual(strip_ansi(result), strip_ansi('\n{PWD}/palmtree/tests/__fixtures__/foo/foo_1.txt\n\n    Not a valid directory: {PWD}/palmtree/tests/__fixtures__/foo/foo_1.txt\n\n'.format(PWD = env.get('PWD'))))

        result = palmtree.inspect(INVALID_FOLDER_PATH, silent = True)

        self.assertEqual(strip_ansi(result), strip_ansi('\n{PWD}/palmtree/tests/__fixtures__/xxx\n\n    Not a valid file/directory: {PWD}/palmtree/tests/__fixtures__/xxx\n\n'.format(PWD = env.get('PWD'))))

        result = palmtree.inspect(INVALID_FILE_PATH, silent = True)

        self.assertEqual(strip_ansi(result), strip_ansi('\n{PWD}/palmtree/tests/__fixtures__/xxx/foo_1.txt\n\n    Not a valid file/directory: {PWD}/palmtree/tests/__fixtures__/xxx/foo_1.txt\n\n'.format(PWD = env.get('PWD'))))

    def test_log(self):
        self.assertTrue(hasattr(palmtree, 'log'))
        self.assertTrue(callable(palmtree.log))

        self.assertEqual(palmtree.log(VALID_FOLDER_PATH), None)
        self.assertEqual(palmtree.log(VALID_FILE_PATH), None)
        self.assertEqual(palmtree.log(INVALID_FOLDER_PATH), None)
        self.assertEqual(palmtree.log(INVALID_FILE_PATH), None)

        def meta(item):
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

        self.assertEqual(palmtree.log(VALID_FOLDER_PATH, meta = meta), None)
        self.assertEqual(palmtree.log(VALID_FILE_PATH, meta = meta), None)
        self.assertEqual(palmtree.log(INVALID_FOLDER_PATH, meta = meta), None)
        self.assertEqual(palmtree.log(INVALID_FILE_PATH, meta = meta), None)


# =========================================
#       MAIN
# --------------------------------------

if __name__ == '__main__':
    helper.run(TestCase)
