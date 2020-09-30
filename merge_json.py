#! /usr/bin/python
# vim: set fileencoding=utf-8 :
#
# --
# Copyright (C) (2020) (Mathieu Bergeron) (mathieu.bergeron@cmontmorency.qc.ca)
# --
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU AFFERO General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
# or see http://www.gnu.org/licenses/agpl.txt.
# --

from __future__ import print_function
import argparse

from libmomo import jsonio
from libmomo.semester import Semester

parser = argparse.ArgumentParser(description='Merge two or more .json file')
parser.add_argument('-i', metavar='IN', type=str, nargs='+', help='One or many input .json files')
parser.add_argument('-o', metavar='OUT', default='merged.json', type=str, help='The output .json file -- defaults to merged.json')

args = parser.parse_args()

if args.i is None:
    parser.print_usage()
    exit(0)

ENCODING = 'utf-8'
INPUT_PATHS = args.i
OUTPUT_PATH = args.o

if __name__ == '__main__':

    semester = None

    for input_path in INPUT_PATHS:

        parsed_semester = jsonio.read_file(ENCODING, input_path)

        if semester is not None:
            semester.merge(parsed_semester)
        else:
            semester = parsed_semester

    jsonio.write_file('utf-8', semester, OUTPUT_PATH)
