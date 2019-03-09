
# coding: utf-8

# =========================================
#       IMPORTS
# --------------------------------------

from __future__ import print_function
from __future__ import unicode_literals

import sys
import os
import re
import inspecta
import mybad

# import chalk as color
import colorful as color

from os import path
from pprint import pprint
from os import environ as env

from attributedict.collections import AttributeDict


# =========================================
#       CONSTANTS
# --------------------------------------

PARENT_PATH = '..'
CURRENT_PATH = '.'
HOME_PATH = '~'

ROOT_LEVEL = 0
# ENV_VARIABLE_PATTERN = r'\$([a-zA-Z_][a-zA-Z0-9_]+)'

DEFAULT_SILENT = False
DEFAULT_INDENT = 4

SPACE = ' '

# BRANCH_PREFIX = '│  '
BRANCH_ITEM_PREFIX = '├── '
BRANCH_ITEM_PREFIX_LAST = '└── '
BRANCH_ITEM_LINK_SUFFIX = ' ⟶  '
BRANCH_ITEM_LINK_BROKEN = '?'


# =========================================
#       ERRORS
# --------------------------------------

class Error(mybad.Error):
    pass


# =========================================
#       FUNCTIONS
# --------------------------------------

def get_tree(root_path = CURRENT_PATH, options = {}, level = ROOT_LEVEL, **kwargs):
    options = dict(options or {}, **kwargs)

    meta = options.get('meta', None)
    silent = options.get('silent', None)

    if silent != False:
        silent = bool(silent) or DEFAULT_SILENT

    items = []

    try:
        root_path = path.abspath(root_path)
        root_path = path.expanduser(root_path)
        root_path = path.expandvars(root_path)

        root_path_stat = None

        try:
            root_path_stat = os.lstat(root_path)

        except Exception as error:
            raise Error('Not a valid file/directory: {root_path}'.format(
                root_path = root_path,
            ))

        if not path.isdir(root_path):
            resolved_root_path = None

            if path.islink(root_path):
                try:
                    resolved_root_path = os.readlink(resolved_root_path)

                except Exception as error:
                    resolved_root_path = None

            if not resolved_root_path:
                raise Error('Not a valid directory: {root_path}'.format(
                    root_path = root_path,
                ))

        file_names = None

        try:
            file_names = os.listdir(root_path)

        except Exception as error:
            raise Error('Could not read directory contents: {root_path}'.format(
                root_path = root_path,
            ))

        for file_name in sorted(file_names):
            file_path = path.join(root_path, file_name)
            relative_file_path = CURRENT_PATH

            absolute_file_path = path.abspath(file_path)
            absolute_file_path = path.expanduser(absolute_file_path)
            absolute_file_path = path.expandvars(absolute_file_path)

            resolved_file_path = str(absolute_file_path)

            file_extension = ('.' in file_name) and '.{0}'.format(file_name.split('.')[-1]) or None

            if file_extension:
                if not len(file_extension):
                    file_extension = None

            file_key = str(file_name)

            if file_extension:
                file_key = file_key.replace(file_extension, '')

            try:
                file_stat = os.lstat(absolute_file_path)

            except Exception as error:
                raise Error('File path don\'t exist: {absolute_file_path}'.format(
                    absolute_file_path = absolute_file_path,
                ))

            is_directory = bool(path.isdir(absolute_file_path))
            is_file = bool(path.isfile(absolute_file_path))
            is_link = bool(path.islink(absolute_file_path))

            is_resolved = True

            if is_link:
                try:
                    previous_resolved_file_path = str(resolved_file_path)

                    resolved_file_path = os.readlink(resolved_file_path)

                    if resolved_file_path.startswith(PARENT_PATH):
                        resolved_file_path = re.sub(r'^[.]{2}', path.dirname(root_path), resolved_file_path)

                    elif resolved_file_path.startswith(CURRENT_PATH):
                        resolved_file_path = re.sub(r'^[.]', root_path, resolved_file_path)

                    resolved_file_path = path.abspath(resolved_file_path)
                    resolved_file_path = path.expanduser(resolved_file_path)
                    resolved_file_path = path.expandvars(resolved_file_path)

                    is_resolved = path.isfile(resolved_file_path) or path.isdir(resolved_file_path)

                    if not is_resolved:
                        resolved_file_path = previous_resolved_file_path

                        raise Exception('Resolved path not valid file/directory')

                except Exception as error:
                    is_resolved = False

            resolved_absolute_file_path = str(resolved_file_path)

            resolved_relative_path = CURRENT_PATH

            if is_link:
                resolved_relative_path = path.relpath(resolved_absolute_file_path, absolute_file_path)

                if resolved_relative_path:
                    if not len(resolved_relative_path):
                        resolved_relative_path = CURRENT_PATH

            resolved_file_name = path.basename(resolved_file_path)
            resolved_file_extension = ('.' in resolved_file_name) and '.{0}'.format(resolved_file_name.split('.')[-1]) or None

            if resolved_file_extension:
                if not len(resolved_file_extension):
                    resolved_file_extension = None

            resolved_file_key = str(resolved_file_name)

            if resolved_file_extension:
                resolved_file_key = resolved_file_key.replace(resolved_file_extension, '')

            is_resolved_directory = bool(path.isdir(resolved_file_path))
            is_resolved_file = bool(path.isfile(resolved_file_path))
            is_resolved_link = bool(path.islink(resolved_file_path))

            item = AttributeDict()

            item.level = level

            item.path = file_path
            item.absolute_path = absolute_file_path
            item.relative_path = relative_file_path
            item.name = file_name
            item.extension = file_extension
            item.key = file_key

            item.resolved_path = resolved_file_path
            item.resolved_absolute_path = resolved_absolute_file_path
            item.resolved_relative_path = resolved_relative_path
            item.resolved_name = resolved_file_name
            item.resolved_extension = resolved_file_extension
            item.resolved_key = resolved_file_key

            item.is_resolved_directory = is_resolved_directory
            item.is_resolved_file = is_resolved_file
            item.is_resolved_link = is_resolved_link

            item.is_directory = is_resolved_directory # ~is_directory
            item.is_file = is_resolved_file # ~is_file
            item.is_link = is_link
            item.is_resolved = is_resolved

            if (is_directory and not is_link):
                try:
                    item.children = get_tree(resolved_file_path, options, level + 1)

                except Exception as error:
                    raise Error('Could not get file system tree: {resolved_file_path}'.format(
                        resolved_file_path = resolved_file_path,
                    ))

            else:
                item.children = None

            meta_data = ''

            if meta and callable(meta):
                try:
                    meta_data = meta(item)

                except Exception as error:
                    raise Error('Could not map item using specified `meta` mapper.')

                if meta_data is None:
                    meta_data = ''

                elif not isinstance(meta_data, str):
                    try:
                        metadata = metadata and json.stringify(metadata)
                        metadata = metadata and color.darkGray(metadata)
                        metadata = str(metadata)

                    except Exception as error:
                        metadata = str(color.red(error))

            elif meta:
                meta_data = meta

            item.meta = meta_data and str(meta_data)

            items.append(item)

        return items

    except Exception as error:
        if not silent:
            raise error

        return items

def inspect_tree(root_path = CURRENT_PATH, options = {}, level = ROOT_LEVEL, **kwargs):
    options = dict(options or {}, **kwargs)

    indent = options.get('indent', None)
    silent = options.get('silent', None)

    if silent != False:
        silent = bool(silent) or DEFAULT_SILENT

    if not indent == False:
        indent = bool(indent) or DEFAULT_INDENT

    else:
        indent = 0

    output = ''

    try:
        if (level == ROOT_LEVEL):
            root_item_name = color.darkGray(root_path)

            output += '\n'
            output += root_item_name

        items = None

        try:
            items = get_tree(root_path, dict(options, **dict(silent = False)))

            if items is None:
                raise Error('Could not get file system tree object: {0}'.format(root_path))

        except Exception as error:
            raise error

        prefix = None

        item_name = None
        item_output = None

        item_count = len(items)
        last_item = items[-1]

        for item in items:
            prefix = indent * level * SPACE

            if item == last_item:
                prefix += color.darkGray(BRANCH_ITEM_PREFIX_LAST)

            else:
                prefix += color.darkGray(BRANCH_ITEM_PREFIX)

            if item.is_directory:
                if item.is_link:
                    item_name = SPACE.join([
                        str(color.bold_white(item.name)),
                        str(color.darkGray(BRANCH_ITEM_LINK_SUFFIX)),
                        str(color.darkGray(item.resolved_relative_path)),
                        str(item.meta),
                    ])

                else:
                    item_name = SPACE.join([
                        str(color.bold_white(item.name)),
                        str(item.meta),
                    ])

            elif item.is_file:
                if item.is_link:
                    item_name = SPACE.join([
                        str(color.white(item.name)),
                        str(color.darkGray(BRANCH_ITEM_LINK_SUFFIX)),
                        str(color.darkGray(item.resolved_relative_path)),
                        str(item.meta),
                    ])

                else:
                    item_name = SPACE.join([
                        str(color.white(item.name)),
                        str(item.meta),
                    ])

            else:
                if item.is_link:
                    item_name = SPACE.join([
                        str(color.red(item.name)),
                        str(color.darkGray(BRANCH_ITEM_LINK_SUFFIX)),
                        str(color.darkGray(BRANCH_ITEM_LINK_BROKEN)),
                        str(item.meta),
                    ])

                else:
                    item_name = SPACE.join([
                        str(color.red(item.name)),
                        str(item.meta),
                    ])

            output += '\n'
            output += prefix
            output += item_name # BUG: unicode issue in Python 2

            if item.children:
                try:
                    item_output = inspect_tree(item.path, options, level + 1)

                except Exception as error:
                    pass

                if isinstance(item_output, str):
                    output += item_output

        if (level == ROOT_LEVEL):
            output += '\n\n'

        return output

    except Exception as error:
        if not silent:
            raise error

        output += '\n\n'
        output += '    {0}'.format(color.red(str(error).split(' - {')[0]))
        output += '\n\n'

        return output


def log_tree(root_path = CURRENT_PATH, options = {}, **kwargs):
    options = dict(options or {}, **kwargs)

    output = inspect_tree(root_path, dict(options, **dict(silent = True)))

    sys.stdout.write(output)


# =========================================
#       EXPORTS
# --------------------------------------

get = get_tree
inspect = inspect_tree
log = log_tree

__all__ = [
    'Error',

    'get',
    'get_tree',

    'inspect',
    'inspect_tree',

    'log',
    'log_tree',

    'color',
]
