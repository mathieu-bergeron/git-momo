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

def columns():
    cols={}

    cols['id'] = {'index':1, 'type':'number', 'unique':True}
    cols['name'] = {'index':2, 'type':'string', 'unique':False}
    cols['group'] = {'index':3, 'type':'number', 'unique':False}
    cols['latestCommit'] = {'index':4, 'type':'date', 'unique':False}
    #cols['latestProject'] = {'index':5, 'type':'date', 'unique':False}
    cols['nbRepos'] = {'index':6, 'type':'number', 'unique':False}
    cols['nbCommits'] = {'index':7, 'type':'number', 'unique':False}
    cols['nbProjects'] = {'index':8, 'type':'number', 'unique':False}

    return cols

