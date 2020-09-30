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
import codecs

import json

import libmomo
from libmomo import semester
from libmomo import jsonio
from libmomo import moodle

#TODO) en français lorsque LANG ou LC_ALL est fr
#import locale
#loc = locale.getlocale()
#print(loc)

parser = argparse.ArgumentParser(description='From Moodle .csv to a .json file')
parser.add_argument('-d', metavar='DATE', default=';', type=str, nargs='?', help='Semester date')
parser.add_argument('-s', metavar='SEP', default=',', type=str, nargs='?', help='The .csv separator -- defaults to ,')
parser.add_argument('-e', metavar='ENC', default='utf-8', type=str, nargs='?', help='Input file encoding -- defaults to utf-8')
parser.add_argument('-i', metavar='CSV', type=str, nargs='+', help='One or many input .csv files (téléchargé via Moodle=>Rapport de questionnaire=>Exporter en format texte)')
parser.add_argument('-o', metavar='JSON', default='moodle.json', type=str, help='The output .json file -- defaults to moodle.json')

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

        parsed_course = moodle.read_file(ENCODING, SEPARATOR, input_path)

        semester.add_or_merge_course(parsed_course)

        jsonio.write_file('utf-8', semester, OUTPUT_PATH)

