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
from tree import Tree

class LocalPath(Tree):

    def __init__(self):
        self.localpath = None

    def dirname(self):
        raise NotImplementedError(self.__class__.__name__)

    def create_file_structure(self, root_path):
        self.localpath = os.path.join(root_path, self.dirname())

        self.mkdir()

        for child in self.children():
            child.create_file_structure(self.localpath)

    def mkdir(self):
        if not os.path.exists(self.localpath):
            os.mkdir(self.localpath)

    def check_localpath(self, action):
        try:
           self.localpath
        except AttributeError:
            raise Exception("[FATAL] localpath not in db.json when attempting to %s %s" % (action, self.url))
