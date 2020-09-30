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

import re

import fuzzywuzzy
from fuzzywuzzy import fuzz
DEFAULT_RATIO=75
STRICT_RATIO=95

from utils import replace_special_chars
from utils import replace_accents
from utils import deregexify

class Matcher(object):

    def __init__(self, pattern):
        pass

    def if_matches(self, string):
        raise NotImplementedError(self.__class__.__name__)

    def if_strictly_matches(self, string):
        raise NotImplementedError(self.__class__.__name__)

    def if_very_strictly_matches(self, string):
        raise NotImplementedError(self.__class__.__name__)

class RegexMatcher(Matcher):

    def __init__(self, pattern):
        super(RegexMatcher, self).__init__(pattern)

        self.matcher = re.compile(replace_accents(pattern))

    def if_matches(self, string):
        matches = self.matcher.search(replace_special_chars(string))
        return matches is not None

    def if_strictly_matches(self, string):
        return self.if_matches(string)

    def if_very_strictly_matches(self, string):
        matches = self.matcher.match(replace_special_chars(string))
        return matches is not None


class FuzzyMatcher(Matcher):
    def __init__(self, pattern, ratio):
        super(FuzzyMatcher, self).__init__(pattern)

        self.target = replace_special_chars(deregexify(pattern))
        self.ratio = ratio


    def if_matches(self, string):
        match_ratio = fuzz.partial_ratio(self.target, replace_special_chars(string))

        return match_ratio >= self.ratio

    def if_strictly_matches(self, string):
        match_ratio = fuzz.ratio(self.target, replace_special_chars(string))

        return match_ratio >= self.ratio

    def if_very_strictly_matches(self, string):
        match_ratio = fuzz.ratio(self.target, replace_special_chars(string))

        return match_ratio >= STRICT_RATIO

class MultiMatcher(Matcher):

    def __init__(self, pattern):
        super(MultiMatcher, self).__init__(pattern)

        self.re_matcher = RegexMatcher(pattern)
        self.fuzzy_matcher = FuzzyMatcher(pattern, DEFAULT_RATIO)

    def if_matches(self, string):
        return self.re_matcher.if_matches(string) or self.fuzzy_matcher.if_matches(string)

    def if_strictly_matches(self, string):
        return self.re_matcher.if_strictly_matches(string) or self.fuzzy_matcher.if_strictly_matches(string)

    def if_very_strictly_matches(self, string):
        return self.re_matcher.if_very_strictly_matches(string) or self.fuzzy_matcher.if_very_strictly_matches(string)
