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

import git
import datetime

from jsonio import JsonIO
from mergeable import Mergeable
from localpath import LocalPath
from project import Project
from commitfinder import CommitFinder

from utils import replace_special_chars



MAIN_BRANCH='master'
EPOCH = datetime.datetime.utcfromtimestamp(0)

class Repo(JsonIO, Mergeable, LocalPath, CommitFinder):

    def __init__(self):
        super(Repo, self).__init__()

        self.url = None
        self.projects = []
        self.student = None
        self.gitrepo = None


    def from_json_map(self, json_map):
        super(Repo, self).from_json_map(json_map)

        if hasattr(self, 'localpath') and os.path.exists(self.localpath):
            try:
                self.gitrepo = git.Repo(self.localpath)
            except git.exc.InvalidGitRepositoryError:
                pass

        for project in self.projects:
            project.repo = self

    def exclude_from_json(self):
        exclusions = super(Repo, self).exclude_from_json()
        exclusions.append('student')
        exclusions.append('gitrepo')
        return exclusions

    def add_or_merge_project(self, project):
        existing_project = self.find_existing_project(project)

        if existing_project is not None:
            existing_project.merge(project)

        else:
            self.projects.append(project)

    def find_existing_project(self, project):
        existing_project = None

        for candidate_project in self.projects:
            if candidate_project.name == project.name:
                existing_project = candidate_project
                break

        return existing_project

    def merge(self, other):
        if self.url != other.url:
            raise Exception("Attemping to merge repos with different urls: %s and %s" % (self.url, other.url))

        for project in other.projects:
            self.add_or_merge_project(project)

        return self

    def dirname(self):
        elements = self.url.split('/')
        dirname = elements[-1]

        if dirname.endswith('.git'):
            dirname = dirname[0:-4]

        dirname = replace_special_chars(dirname)

        return dirname

    def children(self):
        return []

    def check_gitrepo(self, action):
        if self.gitrepo is None:
            raise Exception("[FATAL] gitrepo is None when attempting to %s %s" % (action, self.localpath))

    def clone(self, username, password):
        self.check_localpath("clone repo")

        full_url = self.url.replace('https://','https://%s:%s@'% (username, password))

        try:
            self.gitrepo = git.Repo.clone_from(full_url, self.localpath, branch=MAIN_BRANCH)
            print("cloning %s" % self.student.fullname())
        except:
            print("already cloned for %s" % self.student.fullname())

    def pull(self):
        self.check_gitrepo("pull repo")

        origin = self.gitrepo.remotes[0]

        print("pulling %s" % self.student.fullname())

        origin.pull()

    def extract_email(self):
        self.check_gitrepo("extract email from")

        main_branch = self.gitrepo.heads[0]

        first_commit = list(self.gitrepo.iter_commits(main_branch))[-1]

        self.student.add_or_merge_email(first_commit.committer.email)

    def extract_projects(self, matcher):
        self.check_localpath("extract projects from")

        for project in Project.extract_projects(matcher, self.localpath):
            project.repo = self
            self.add_or_merge_project(project)

    def find_projects(self, matcher):
        for project in self.projects:
            if matcher.if_matches(project.name):
                yield project

    def unix_commit_date(self, commit):
        return commit.committed_date * 1000

    def latest_commit(self):
        commit = self.gitrepo.head.commit
        date = "N/A"

        if commit is not None:
            date = self.unix_commit_date(commit)

        return date

    def latest_project(self):
        latest_project = {'date':0, 'name': 'FIXME'}
        return latest_project

        # FIXME) below does not work
        main_branch = self.gitrepo.heads[0]


        for commit in self.gitrepo.iter_commits():
            candidate = self.latest_project_for_commit(commit)
            if candidate is not None:
                latest_project = candidate
                break;

        return latest_project

    def is_empty_commit(self, commit):
        stats = commit.stats
        return stats.total['lines'] != 0

    def latest_project_for_commit(self, commit):
        latest_project = None

        if not self.is_empty_commit(commit):
            for obj in commit.tree.traverse():
                if obj.path is not None:
                    project = self.project_that_includes_path(obj.path)
                    if project is not None:
                        latest_project = {'date': self.unix_commit_date(commit), 'name': project.name}
                        break;

        return latest_project

    def project_that_includes_path(self, path):
        result = None
        for project in self.projects:
            if path in project.localpath:
                result = project
                break;

        return result


    def number_of_projects(self):
        return len(self.projects)

    def number_of_commits(self):
        number = 0
        for commit in self.gitrepo.iter_commits():
            number += 1

        return number

    def find_commits(self, matcher):
        for commit in self.gitrepo.iter_commits():
            if matcher.if_matches(commit.message):
                yield commit
