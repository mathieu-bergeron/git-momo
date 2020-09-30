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
import os

from libmomo import jsonio
from libmomo.semester import Semester
from libmomo.clone import create_file_structure
from libmomo.clone import clone_all

parser = argparse.ArgumentParser(description='Clone repos found in db.json ; write updates to output .json file')
parser.add_argument('-i', metavar='IN', default='db.json', type=str, help='Input .json file -- defaults to db.json')
parser.add_argument('-o', metavar='OUT', type=str, nargs='?', help='Output .json file -- defaults to input .json file')
parser.add_argument('-u', metavar='USER', type=str, nargs='?', help='GitHub username')
parser.add_argument('-p', metavar='PASS', type=str, nargs='?', help='GitHub password')

args = parser.parse_args()

if args.i is None:
    parser.print_usage()
    exit(0)

ENCODING = 'utf-8'
INPUT_PATH = args.i
OUTPUT_PATH = args.o
if OUTPUT_PATH is None:
    OUTPUT_PATH = INPUT_PATH
USERNAME = args.u
PASSWORD = args.p

if __name__ == '__main__':

    semester = jsonio.read_file(ENCODING, INPUT_PATH)

    semester.create_file_structure(os.getcwd())

    jsonio.write_file(ENCODING, semester, OUTPUT_PATH)

    for repo in semester.find_all_repos():
        repo.clone(USERNAME, PASSWORD)


