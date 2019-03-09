
# coding: utf-8

# ==========================================================
#       IMPORTS
# ----------------------------------------------------

import rootpath

rootpath.append()

import palmtree

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
