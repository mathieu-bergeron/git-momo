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
import shutil

def initialize_dir(dirpath):
    if os.path.exists(dirpath):
        shutil.rmtree(dirpath)

    os.mkdir(dirpath)

def replace_special_chars(value):
    value = replace_accents(value)
    value = value.replace('.','')
    value = value.replace('-','')
    value = value.replace("'",'')
    value = value.replace(' ','_')

    return value

def replace_accents(value):
    value = value.replace(u'é','e')
    value = value.replace(u'è','e')
    value = value.replace(u'ê','e')
    value = value.replace(u'à','a')
    value = value.replace(u'â','a')
    value = value.replace(u'î','i')
    value = value.replace(u'ô','o')
    value = value.replace(u'ë','e')
    value = value.replace(u'ï','i')

    return value

def deregexify(pattern):

    pattern = pattern.replace('*','')
    pattern = pattern.replace('.','')
    pattern = pattern.replace('[','')
    pattern = pattern.replace(']','')
    pattern = pattern.replace(')','')
    pattern = pattern.replace('(','')
    pattern = pattern.replace('|','')
    pattern = pattern.replace('+','')
    pattern = pattern.replace('?','')

    return pattern
