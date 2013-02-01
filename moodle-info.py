#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Moodle Development Kit

Copyright (c) 2012 Frédéric Massart - FMCorz.net

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

http://github.com/FMCorz/mdk
"""

import sys
import argparse
from lib import workplace
from lib.tools import debug

Wp = workplace.Workplace()

# Arguments
parser = argparse.ArgumentParser(description='Display information about a Moodle instance')
parser.add_argument('-l', '--list', action='store_true', help='list the instances', dest='list')
parser.add_argument('-i', '--integration', action='store_true', help='used with --list, only display integration instances', dest='integration')
parser.add_argument('-s', '--stable', action='store_true', help='used with --list, only display stable instances', dest='stable')
parser.add_argument('-n', '--name-only', action='store_true', help='used with --list, only display instances name', dest='nameonly')
parser.add_argument('-v', '--var', metavar='var', default=None, nargs='?', help='variable to output or edit')
parser.add_argument('-e', '--edit', metavar='value', nargs='?', help='value to set to the variable (--var). This value will be set in the config file of the instance. Prepend the value with i: or b: to set as int or boolean. DO NOT use names used by MDK (identifier, stablebranch, ...).', dest='edit')
parser.add_argument('name', metavar='name', default=None, nargs='?', help='name of the instance')
args = parser.parse_args()

# List the instances
if args.list:
    if args.integration != False or args.stable != False:
        l = Wp.list(integration=args.integration, stable=args.stable)
    else:
        l = Wp.list()
    l.sort()
    for i in l:
        if not args.nameonly:
            M = Wp.get(i)
            print '{0:<25}'.format(i), M.get('release')
        else:
            print i

# Loading instance
else:
    M = Wp.resolve(args.name)
    if not M:
        debug('This is not a Moodle instance')
        sys.exit(1)

    # Printing/Editing variable.
    if args.var != None:
        # Edit a value.
        if args.edit != None:
            val = args.edit
            if val.startswith('b:'):
                val = True if val[2:].lower() in ['1', 'true'] else False
            elif val.startswith('i:'):
                try:
                    val = int(val[2:])
                except ValueError:
                    # Not a valid int, let's consider it a string.
                    pass
            M.updateConfig(args.var, val)
            debug('Set $CFG->%s to %s on %s' % (args.var, str(val), M.get('identifier')))
        else:
            print M.get(args.var)

    # Printing info
    else:
        for key, info in M.info().items():
            print '{0:<20}: {1}'.format(key, info)
