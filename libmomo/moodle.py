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

import codecs

from course import Course
from group import Group
from student import Student
from repo import Repo

MOODLENAME_POSITION=7
COURSE_GROUP_POSITION=5
REPO_URL_POSITION=9

def read_file(encoding, separator, input_path):

    course = None

    with codecs.open(input_path, encoding=encoding) as input_file:
        # skip first line
        input_file.readline()

        course = read_students(separator, input_file)

    return course

def read_students(separator, input_file):

    course = None

    for input_line in input_file:

        student_course = read_student_course(separator, input_line.rstrip())

        if course is None:
            course = student_course
        else:
            course.merge(student_course)

    return course

def read_student_course(separator, input_line):
    course = Course()
    group = Group()
    student = Student()
    repo = Repo()

    elements = input_line.split(separator)

    course_group = elements[COURSE_GROUP_POSITION]
    moodlename = elements[MOODLENAME_POSITION].replace('"','')
    git_url = elements[REPO_URL_POSITION]

    course_group_elements = course_group.split('-')
    course_code = course_group_elements[3]
    group_number = int(course_group_elements[4])

    repo.url = git_url
    student.moodlename = moodlename
    group.number = group_number
    course.code = course_code

    student.add_or_merge_repo(repo)
    group.add_or_merge_student(student)
    course.add_or_merge_group(group)

    return course






