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

from __future__ import print_function
import argparse
import os
import shutil
import codecs
import re
import json

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import mpld3

from datetime import datetime
from datetime import timedelta

from libmomo import jsonio
from libmomo.semester import Semester
from libmomo.clone import create_file_structure
from libmomo.clone import clone_all
from libmomo.utils import initialize_dir


parser = argparse.ArgumentParser(description='Progress report for students in of db.json')
parser.add_argument('-i', metavar='IN', default='db.json', type=str, help='Input .json file -- defaults to db.json')
parser.add_argument('-o', metavar='OUTDIR', type=str, help='Output dir -- defaults to progress_report')
parser.add_argument('-b', metavar='BROWSER', type=str, help='Path to browser executable')

args = parser.parse_args()

if args.i is None:
    parser.print_usage()
    exit(0)

ENCODING = 'utf-8'
INPUT_PATH = args.i
if args.o is not None:
    OUTPUT_DIR = args.o
else:
    OUTPUT_DIR = 'progress_report'
BROWSER_PATH = args.b

HTMLNAME='index.html'

START_DATE = datetime(2020, 8, 23)
END_DATE = datetime.now() + timedelta(days=1)

MAX_COMMIT_SIZE=350

earliest_commit = None
latest_commit = None
commit_labels = []
commit_dates = []
commit_sizes = []

def initialize_fig():
    global earliest_commit
    global latest_commit
    global x_labels
    global commit_labels
    global commit_dates
    global commit_sizes

    earliest_commit = None
    latest_commit = None
    commit_labels = []
    commit_dates = []
    commit_sizes = []

def analyze_commit(commit):
    global earliest_commit
    global latest_commit
    global x_labels
    global commit_labels
    global commit_dates
    global commit_sizes

    size = commit.stats.total['lines']
    date = datetime.fromtimestamp(commit.committed_date)
    label = commit.message

    if latest_commit is None or date > latest_commit:
        latest_commit = date

    if earliest_commit is None or date < earliest_commit:
        earliest_commit = date

    commit_dates.append(date)
    commit_sizes.append(size)
    commit_labels.append(label)

def create_fig():
    plt.margins(0)

    fig, ax = plt.subplots(figsize=(14,5))

    plt.ylim(bottom=-30, top=MAX_COMMIT_SIZE+30)
    plt.xlim(left=START_DATE, right=END_DATE)

    ax.grid(True, alpha=0.3)

    x_ticks = []
    x_labels = []
    i_date = START_DATE
    i_label = 0
    while i_date <= END_DATE:
        x_ticks.append(i_date)
        if i_label % 5 == 0:
            x_labels.append(i_date.strftime('%d-%m'))
        else:
            x_labels.append('')

        i_date += timedelta(days=1)
        i_label += 1

    plt.xticks(x_ticks, x_labels, rotation=90)
    plt.yticks(xrange(-30,MAX_COMMIT_SIZE+30,10),[])

    points = ax.stem(commit_dates, commit_sizes)
    tooltip = mpld3.plugins.PointHTMLTooltip(points[0], labels=commit_labels)
    mpld3.plugins.connect(fig, tooltip)

    return fig


def progress_report_for_student(student):
    dirpath = os.path.join(student.localpath, OUTPUT_DIR)
    output_path = os.path.join(dirpath, HTMLNAME)

    print("Writing %s" % output_path)

    initialize_dir(dirpath)

    initialize_fig()

    for commit in student.find_all_commits():
        analyze_commit(commit)

    if len(commit_dates) > 0:
        fig = create_fig()

        with codecs.open(output_path,'w', encoding='utf8') as output_file:
            mpld3.save_html(fig, output_file)

        plt.close()

    else:
        with codecs.open(output_path,'w', encoding='utf8') as output_file:
            output_file.write("<h1>No repo</h1>")

if __name__ == '__main__':

    semester = jsonio.read_file(ENCODING, INPUT_PATH)

    for student in semester.find_all_students():
        progress_report_for_student(student)
