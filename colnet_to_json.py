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

import libmomo
from libmomo import colnet
from libmomo import jsonio
from libmomo import semester

parser = argparse.ArgumentParser(description='From ColNet .csv format to a .json file')
parser.add_argument('-d', metavar='DATE', default=';', type=str, nargs='?', help='Semester date')
parser.add_argument('-s', metavar='SEP', default=';', type=str, nargs='?', help='The .csv separator -- defaults to ;')
parser.add_argument('-e', metavar='ENC', default='latin1', type=str, nargs='?', help='Input file encoding -- defaults to latin1')
parser.add_argument('-i', metavar='CSV', type=str, nargs='+', help='One or many input .csv files (téléchargé via ColNet=>Liste de classe=>Télécharger la liste de classe)')
parser.add_argument('-o', metavar='JSON', default='colnet.json', type=str, help='The output .json file -- defaults to colnet.json')

args = parser.parse_args()

if args.i is None:
    parser.print_usage()
    exit(0)

DATE = args.d
ENCODING = args.e
SEPARATOR = args.s
INPUT_PATHS = args.i
OUTPUT_PATH = args.o

if __name__ == '__main__':

    semester = semester.Semester()
    semester.date = DATE

    for input_path in INPUT_PATHS:

        course = colnet.read_file(ENCODING, SEPARATOR, input_path)

        semester.add_or_merge_course(course)

        jsonio.write_file('utf-8', semester, OUTPUT_PATH)
