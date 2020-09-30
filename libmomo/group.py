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

from jsonio import JsonIO
from mergeable import Mergeable
from localpath import LocalPath
from repofinder import RepoFinder
from projectfinder import ProjectFinder
from studentfinder import StudentFinder

class Group(JsonIO, Mergeable, LocalPath, RepoFinder, ProjectFinder, StudentFinder):

    def __init__(self):
        super(Group, self).__init__()

        self.number = None
        self.course = None
        self.students = []

    def exclude_from_json(self):
        exclusions = super(Group, self).exclude_from_json()
        exclusions.append("course")
        return exclusions

    def from_json_map(self, json_map):
        super(Group, self).from_json_map(json_map)

        for student in self.students:
            student.group = self

    def add_or_merge_student(self, student):
        existing_student = self.find_existing_student(student)

        if existing_student is not None:
            existing_student.merge(student)

        else:
            self.students.append(student)
            student.group = self

    def find_existing_student(self, student):
        existing_student = None

        for candidate_student in self.students:
            if (candidate_student.registration_id is not None and candidate_student.registration_id == student.registration_id) \
               or (candidate_student.moodlename is not None and candidate_student.moodlename == student.moodlename):

                existing_student = candidate_student
                break

        return existing_student

    def merge(self, other):
        if self.number != other.number:
            raise Exception("Attempting to merge groups with different numbers: %s and %s" % (self.number, other.number))

        for student in other.students:
            self.add_or_merge_student(student)

        return self

    def dirname(self):
        return "%02d" % self.number

    def children(self):
        return self.students

    def find_students(self, matcher):
        for student in self.students:
            if matcher.if_matches(student.fullname())  \
               or matcher.if_matches(student.registration_id)  \
               or matcher.if_matches(student.linux_id) \
               or matcher.if_matches(student.anon_id):

                yield student


