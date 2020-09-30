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
import json

import libmomo
from libmomo import *

TYPE_KEY='_T'

def write_file(encoding, data, output_path):
    with codecs.open(output_path, 'w', encoding=encoding) as output_file:
        output_file.write(data.to_json())

def read_file(encoding, input_path):
    with codecs.open(input_path, encoding=encoding) as input_file:
        json_map = json.loads(input_file.read())

        return from_json_map(json_map)

def from_json_map(json_map):

    _type = json_map[TYPE_KEY]
    _module = __import__('libmomo')
    _class = getattr(_module, _type)

    obj = _class()
    obj.from_json_map(json_map)

    return obj

def to_json_value(value):
    json_value = value

    if hasattr(value, 'to_json_map'):
        to_json_map = getattr(value, 'to_json_map')
        if callable(to_json_map):
            json_value = to_json_map()

    elif type(value) == list:
        json_value = [to_json_value(item) for item in value]

    elif type(value) == dict:
        json_value = {}
        for key in value:
            json_value[key] = to_json_value(value[key])

    return json_value

def to_python_value(json_value):
    python_value = json_value

    if type(json_value) == dict:
        python_value = from_json_map(json_value)

        if hasattr(python_value, 'from_json_map'):
            python_value.from_json_map(json_value)

    elif type(json_value) == list:
        python_value = [to_python_value(item) for item in json_value]

    return python_value

class JsonIO(object):

    def __init__(self):
        setattr(self, TYPE_KEY, self.__class__.__name__)

    def to_json(self):
        return json.dumps(self.to_json_map(), sort_keys=True, indent=4, ensure_ascii=False)

    def exclude_from_json(self):
        return []

    def to_json_map(self):
        json_map = {}

        for key in self.__json_keys():
            json_map[key] = to_json_value(getattr(self, key))

        return json_map

    def __json_keys(self):
        exclusions = self.exclude_from_json()

        return [key for key in self.__dict__ if key not in exclusions]

    def from_json_map(self, json_map):
        for key in json_map:
            setattr(self, key, to_python_value(json_map[key]))

    def __str__(self):
        return "{" + ",".join(["%s:%s" % (key, self.__dict__[key]) for key in self.__json_keys()]) + "}"
