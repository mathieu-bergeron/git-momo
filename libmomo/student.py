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
from repofinder import RepoFinder
from projectfinder import ProjectFinder
from commitfinder import CommitFinder
from status_report import columns

from utils import replace_special_chars

class Student(JsonIO, Mergeable, LocalPath, RepoFinder, ProjectFinder, CommitFinder):

    def __init__(self):
        super(Student, self).__init__()

        self.registration_id = None
        self.surname = None
        self.name = None
        self.moodlename = None
        self.program = None
        self.emails = []
        self.phone = None
        self.linux_id = None
        self.group = None
        self.repos = []

    def exclude_from_json(self):
        exclusions = super(Student, self).exclude_from_json()
        exclusions.append("group")
        return exclusions

    def from_json_map(self, json_map):
        super(Student, self).from_json_map(json_map)

        for repo in self.repos:
            repo.student = self

    def add_or_merge_email(self, email):
        # TODO) a merge based on approximate matching?
        #       warn if two emails are very similar (perhaps a typo)
        if email not in self.emails:
            self.emails.append(email)

    def add_or_merge_repo(self, repo):
        existing_repo = self.find_repo(repo)
        
        if existing_repo is not None:
            existing_repo.merge(repo)

        else:
            self.repos.append(repo)

    def find_repo(self, repo):
        existing_repo = None

        for candidate_repo in self.repos:
            if candidate_repo.url == repo.url:
                existing_repo = candidate_repo
                break

        return existing_repo

    def merge(self, other):
        if other.registration_id is not None and self.registration_id != other.registration_id:
            raise Exception("Attemping to merge students with different registration_id: %s and %s" % (self.registration_id, other.registration_id))

        for email in other.emails:
            self.add_or_merge_email(course)

        for repo in other.repos:
            self.add_or_merge_repo(repo)

        return self


    def __getattribute__(self, name):
        if name == 'courses':
            return [group.course for group in groups]
        else:
            return object.__getattribute__(self, name)

    def dirname(self):
        dirname = "%s_%s" % (self.name, self.surname)
        dirname = replace_special_chars(dirname)

        return dirname

    def fullname(self):
        return "%s %s" % (self.name, self.surname)

    def children(self):
        return self.repos

    def find_repos(self, matcher):
        if matcher.if_very_strictly_matches(self.name) \
           or matcher.if_very_strictly_matches(self.surname) \
           or matcher.if_very_strictly_matches(str(self.registration_id)):
            for repo in self.repos:
                yield repo

    def status_report_row(self):
        row = {}

        for colname in columns():
            if colname == 'id':
                row[colname] = self.registration_id
            elif colname == 'name':
                row[colname] = '<a href="%s" target="_blank">%s</a>' % (os.path.join("..",self.group.dirname(),self.dirname(),"progress_report","index.html"), self.fullname())
            elif colname == 'group':
                row[colname] = self.group.number
            elif colname == 'latestCommit':
                row[colname] = self.latest_commit()
            elif colname == 'latestProject':
                row[colname] = self.latest_project()
            elif colname == 'nbRepos':
                row[colname] = self.number_of_repos()
            elif colname == 'nbCommits':
                row[colname] = self.number_of_commits()
            elif colname == 'nbProjects':
                row[colname] = self.number_of_projects()

        return row

    def latest_commit(self):
        latest_commit = "N/A"

        latest_commits = [repo.latest_commit() for repo in self.repos]

        if len(latest_commits) > 0:
            latest_commit = max(latest_commits)

        return latest_commit


    def latest_project(self):
        latest_project = {'name':"N/A"}
        latest_projects = [repo.latest_project() for repo in self.repos]

        if len(latest_projects) > 0:
            latest_project = max(latest_projects, key=lambda project: project['date'])

        return latest_project['name']

    def number_of_repos(self):
        number_of_repos = len(self.repos)
        if number_of_repos == 0:
            number_of_repos = "N/A"

        return number_of_repos

    def number_of_commits(self):
        number_of_commits = sum([repo.number_of_commits() for repo in self.repos])
        if number_of_commits == 0:
            number_of_commits = "N/A"

        return number_of_commits

    def number_of_projects(self):
        number_of_projects = sum([repo.number_of_projects() for repo in self.repos])
        if number_of_projects == 0:
            number_of_projects = "N/A"

        return number_of_projects
