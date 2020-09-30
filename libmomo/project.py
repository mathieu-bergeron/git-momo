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

from jsonio import JsonIO
from mergeable import Mergeable
from localpath import LocalPath

class Project(JsonIO, Mergeable, LocalPath):

    @classmethod
    def extract_projects(cls, matcher, path):
        for projectpath, subdirs, files in os.walk(path):
            project_name = os.path.basename(projectpath)
            if Project.__is_project_to_extract(matcher, project_name, projectpath):
                project = Project()
                project.name = project_name
                project.localpath = projectpath
                yield project

    @classmethod
    def __is_project_to_extract(cls, matcher, project_name, path):
        return matcher.if_matches(project_name) and Project.__is_a_project_path(path)

    @classmethod
    def __is_a_project_path(cls, path):
        java_src = os.path.join(path, "src")
        android_src = os.path.join(path, "app", "src")

        return os.path.exists(java_src) or os.path.exists(android_src)

    def __init__(self):
        super(Project, self).__init__()

        self.name = None
        self.repo = None

    def exclude_from_json(self):
        exclusions = super(Project, self).exclude_from_json()
        exclusions.append('repo')
        return exclusions

    def merge(self, other):
        if self.name != other.name:
            raise Exception("Attemping to merge projects with different names: %s and %s" % (self.name, other.name))

        pass

    def find_files(self, matcher):
        self.check_localpath("finding files")

        for root, subdirs, files in os.walk(self.localpath):
            for filename in files:
                if matcher.if_matches(filename):
                    filepath = os.path.join(self.localpath, root, filename)
                    yield filepath
