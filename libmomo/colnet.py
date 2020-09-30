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
import random
import re

from course import Course
from group import Group
from student import Student
from utils import replace_special_chars

POSITION_SURNAME = 0
POSITION_NAME = 1
POSITION_REGISTRATION_ID = 2
POSITION_PROGRAM = 3
POSITION_NOTE = 4
POSITION_PHONE = 5


def read_file(encoding, separator, input_path):

    course = Course()

    with codecs.open(input_path, encoding=encoding) as input_file:
        group = parse_first_line(course, input_file.readline().rstrip())
        read_students(group, separator, input_file)

        course.add_or_merge_group(group)

    return course

def parse_first_line(course, first_line):
    elements = first_line.split(' ')

    code_group = elements[1].split('-')

    course.code = code_group[0]
    course.title = " ".join(elements[2:])

    group = Group()
    group.number = int(code_group[1])

    return group


def read_students(group, separator, input_file):
    for line in input_file:
        student = Student()

        fields = line.split(separator)
        student.name = fields[POSITION_NAME].rstrip()
        student.surname = fields[POSITION_SURNAME].rstrip()
        student.moodlename = "%s %s" % (student.surname, student.name)
        student.registration_id = fields[POSITION_REGISTRATION_ID].rstrip()
        student.program = fields[POSITION_PROGRAM].rstrip()
        student.comment = fields[POSITION_NOTE].rstrip()
        student.phone = fields[POSITION_PHONE].rstrip()
        student.linux_id = linux_id(student)
        student.anon_id = anon_id()

        group.add_or_merge_student(student)

linux_ids = {}
def linux_id(student):
    global linux_ids

    fullname = student.fullname()

    splitter = re.compile("(\\s|[-_'])")

    elements = splitter.split(fullname)

    elements = [element for element in elements if element != ' ']

    per_element = 2 if len(elements) > 2 else 3

    elements = [element[0:per_element] for element in elements]

    _id = "".join(elements)

    _id = _id.lower()

    _id = replace_special_chars(_id)

    _id = make_unique(linux_ids, _id)

    linux_ids[_id] = True

    return _id

anon_ids = {}
def anon_id():
    global anon_ids

    _id = ""

    for x in xrange(5):
        _id += random.choice("abcdefghijklmnopqrstuvwxyz")

    _id = make_unique(anon_ids, _id)

    anon_ids[_id] = True

    return _id


def make_unique(ids, _id):
    while ids.has_key(_id):
        to_replace = random.randint(0,len(_id)-1)
        _id = _id[0:to_replace] + random.choice("abcdefghijklmnopqrstuvwxyz")  + _id[to_replace:-1]

    return _id
