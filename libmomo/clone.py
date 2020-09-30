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

import os

from utils import replace_special_chars

def create_file_structure(semester):

    root_path = os.path.join(semester.date)

    mkdir(root_path)

    for course in semester.courses:
        course_path = os.path.join(root_path, course.code)

        mkdir(course_path)

        for group in course.groups:

            group_string = "%02d" % group.number

            group_path = os.path.join(course_path, group_string)

            mkdir(group_path)

            for student in group.students:

                dirname = student_dirname(student)

                student_path = os.path.join(group_path, dirname)

                mkdir(student_path)

def student_dirname(student):
    student_dirname = "%s_%s" % (student.name, student.surname)
    student_dirname = replace_special_chars(student_dirname)

    return student_dirname

def mkdir(path):
    if not os.path.exists(path):
        os.mkdir(path)

def clone_all(semester, username, password):
    pass
