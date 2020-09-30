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

class Course(JsonIO, Mergeable, LocalPath, RepoFinder, ProjectFinder, StudentFinder):

    def __init__(self):
        super(Course, self).__init__()

        self.title = None
        self.code = None
        self.groups = []

    def from_json_map(self, json_map):
        super(Course, self).from_json_map(json_map)

        for group in self.groups:
            group.course = self

    def add_or_merge_group(self, group):
        existing_group = self.find_group(group)

        if existing_group is not None:
            existing_group.merge(group)

        else:
            self.groups.append(group)

    def find_group(self, group):
        existing_group = None

        for candidate_group in self.groups:
            if candidate_group.number == group.number:
                existing_group = candidate_group
                break

        return existing_group

    def merge(self, other):
        if self.code != other.code:
            raise Exception("Attempting to merge courses with different codes: %s and %s" % (self.code, other.code))

        for group in other.groups:
            self.add_or_merge_group(group)

        return self

    def dirname(self):
        return self.code

    def children(self):
        return self.groups

