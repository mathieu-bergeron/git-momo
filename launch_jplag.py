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
import re
import shutil

from libmomo import jsonio
from libmomo.semester import Semester
from libmomo.clone import create_file_structure
from libmomo.clone import clone_all
from libmomo.matchers import RegexMatcher
from libmomo.utils import deregexify
from libmomo.utils import replace_special_chars

parser = argparse.ArgumentParser(description='Collect *.java of some project -- launch jplag')
parser.add_argument('-i', metavar='IN', default='db.json', type=str, help='Input .json file -- defaults to db.json')
parser.add_argument('-o', metavar='OUTDIR', type=str, help='Output dir -- defaults to pattern')
parser.add_argument('-p', metavar='PATTERN', type=str, help='Regex pattern used to select project')
parser.add_argument('-e', metavar='EXCLUDE', default=None, type=str, help='Regex pattern used to exclude files')
parser.add_argument('-j', metavar='JAVA', default='java', type=str, help='Path to java executable -- defaults to java')
parser.add_argument('-jplag', metavar='JPLAG', type=str, help='Path to jplag .jar file')
parser.add_argument('-jplagargs', metavar='JPLAGARGS', type=str, help='Extra arguments to jplag')
parser.add_argument('-b', metavar='BROWSER', type=str, help='Path to browser executable')

args = parser.parse_args()

if args.i is None or args.p is None:
    parser.print_usage()
    exit(0)

ENCODING = 'utf-8'
INPUT_PATH = args.i
PATTERN = args.p
if args.o is not None:
    OUTPUT_DIR = args.o
else:
    OUTPUT_DIR = replace_special_chars(deregexify(PATTERN))
FILES_DIR = 'files'
RESULT_DIR = 'result'
JAVAPATH = args.j
JPLAGPATH = args.jplag
if args.jplagargs is not None:
    JPLAGARGS = args.jplagargs
else:
    JPLAGARGS = " "
EXCLUDE_PATTERN = args.e
BROWSER_PATH = args.b
INDEX_NAME='index.html'
JAVA_PATTERN='[Jj][Aa][Vv][Aa]$'

courses = {}
def initialize_course(course):
    global courses

    if not course in courses:
        outputpath = os.path.join(course.localpath, OUTPUT_DIR)
        filespath = os.path.join(outputpath, FILES_DIR)

        if os.path.exists(outputpath):
            shutil.rmtree(outputpath)

        os.mkdir(outputpath)
        os.mkdir(filespath)

        courses[course] = outputpath

def delete_excluded_files(path, exclusion_matcher):
    for root, subdirs, files in os.walk(path):
        for filename in files:
            if exclusion_matcher.if_matches(filename):
                filepath = os.path.join(root, filename)
                os.remove(filepath)

if __name__ == '__main__':

    semester = jsonio.read_file(ENCODING, INPUT_PATH)

    project_matcher = RegexMatcher(PATTERN)
    java_matcher = RegexMatcher(JAVA_PATTERN)
    if EXCLUDE_PATTERN is not None:
        exclusion_matcher = RegexMatcher(EXCLUDE_PATTERN)

    for project in semester.find_projects(project_matcher):
        course = project.repo.student.group.course
        initialize_course(course)

        outputpath = courses[course]
        filespath = os.path.join(outputpath, FILES_DIR)

        student_path = os.path.join(filespath, project.repo.student.anon_id)
        os.mkdir(student_path)

        for srcpath in project.find_files(java_matcher):
            srcname = os.path.basename(srcpath)
            destpath = os.path.join(student_path, srcname)
            shutil.copy(srcpath, destpath)

    for course in courses:
        outputpath = courses[course]
        filespath = os.path.join(outputpath, FILES_DIR)
        resultpath = os.path.join(outputpath, RESULT_DIR)
        indexpath = os.path.join(resultpath, INDEX_NAME)

        print("Files collected to %s" % filespath)

        # exclude files
        if EXCLUDE_PATTERN is not None:
            delete_excluded_files(filespath, exclusion_matcher)

        # launch jplag
        jplag_cmd = "%s -jar %s -l java19 %s %s -r %s >/dev/null 2>/dev/null" % (JAVAPATH, JPLAGPATH, JPLAGARGS, filespath, resultpath)
        #print("launching jplag: %s" % jplag_cmd)
        os.system(jplag_cmd)

        print("jplag results written to %s" % indexpath)


        if BROWSER_PATH is not None:
            browser_cmd = "%s %s" % (BROWSER_PATH, indexpath)
            print("launching browser")
            os.system(browser_cmd)




