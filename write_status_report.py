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
import shutil
import codecs
import re
import json

from libmomo import jsonio
from libmomo.semester import Semester
from libmomo.clone import create_file_structure
from libmomo.clone import clone_all
from libmomo.status_report import columns

parser = argparse.ArgumentParser(description='Status report for students in of db.json')
parser.add_argument('-i', metavar='IN', default='db.json', type=str, help='Input .json file -- defaults to db.json')
parser.add_argument('-o', metavar='OUTDIR', type=str, help='Output dir -- defaults to status_report')
parser.add_argument('-b', metavar='BROWSER', type=str, help='Path to browser executable')

args = parser.parse_args()

if args.i is None:
    parser.print_usage()
    exit(0)

ENCODING = 'utf-8'
INPUT_PATH = args.i
if args.o is not None:
    OUTPUT_DIR = args.o
else:
    OUTPUT_DIR = 'status_report'
BROWSER_PATH = args.b

HTML_SRC='html_src'
JSNAME='jquery.watable.js'
CSSNAME='watable.css'
HTMLNAME='index.html'

def copy_watable_files(destdirpath):
    srcpath = os.path.join(HTML_SRC, JSNAME)
    destpath = os.path.join(destdirpath, JSNAME)
    shutil.copy(srcpath, destpath)

    srcpath = os.path.join(HTML_SRC, CSSNAME)
    destpath = os.path.join(destdirpath, CSSNAME)
    shutil.copy(srcpath, destpath)

def initialize_dir(dirpath):
    if os.path.exists(dirpath):
        shutil.rmtree(dirpath)

    os.mkdir(dirpath)

def write_html_file(course, destdirpath, data):
    input_path = os.path.join(HTML_SRC, HTMLNAME)
    output_path = os.path.join(destdirpath, HTMLNAME)

    variable_pattern = '\\$[A-Z]+'
    variable_matcher = re.compile(variable_pattern)

    with codecs.open(input_path, encoding=ENCODING) as input_file:
        with codecs.open(output_path, 'w', encoding=ENCODING) as output_file:
            for line in input_file:
                matches = variable_matcher.search(line)
                if matches is not None:
                    match = matches.group(0)
                    if match == '$COURSE':
                        line = line.replace('$COURSE', course.code)
                    elif match == '$DATA':
                        line = line.replace('$DATA', json.dumps(data, sort_keys=True, indent=24, ensure_ascii=False))

                output_file.write(line)

    print('Written %s' % output_path)

def status_report_for_course(course):
    dirpath = os.path.join(course.localpath, OUTPUT_DIR)

    initialize_dir(dirpath)
    copy_watable_files(dirpath)

    cols = columns()

    rows = []

    for student in course.find_all_students():
        student_row = student.status_report_row()
        rows.append(student_row)

    data = {}

    data['cols'] = cols
    data['rows'] = rows

    write_html_file(course, dirpath, data)

    htmlpath = os.path.join(dirpath, HTMLNAME)

    if BROWSER_PATH is not None:
        print('Launching browser on %s' % htmlpath)
        os.system('%s %s' % (BROWSER_PATH, htmlpath))


if __name__ == '__main__':

    semester = jsonio.read_file(ENCODING, INPUT_PATH)

    for course in semester.courses:
        status_report_for_course(course)
