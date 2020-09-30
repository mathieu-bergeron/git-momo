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

class Semester(JsonIO, Mergeable, LocalPath, RepoFinder, ProjectFinder, StudentFinder):

    def __init__(self):
        super(Semester, self).__init__()

        self.date = None
        self.courses = []

    def add_or_merge_course(self, course):
        existing_course = self.find_course(course)

        if existing_course is not None:
            existing_course.merge(course)
        else:
            self.courses.append(course)

    def find_course(self, course):
        existing_course = None

        for candidate_course in self.courses:
            if candidate_course.code == course.code:
                existing_course = candidate_course
                break

        return existing_course

    def merge(self, other):
        if self.date != other.date:
            raise Exception("Attemping to merge semesters with different dates: %s and %s" % (self.date, other.date))

        for course in other.courses:
            self.add_or_merge_course(course)

        return self

    def dirname(self):
        return self.date

    def children(self):
        return self.courses

