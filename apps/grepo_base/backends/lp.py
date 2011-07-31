#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    grepo_base.backends.lp
    ~~~~~~~~~~~~~~~~~

    Launchpad backend for `grepo`.
"""

import re
import posixpath
from datetime import datetime
import math

from django.conf import settings

from launchpadlib.launchpad import Launchpad

from grepo_base.models import Language

STATES = (
    'New',
    'Incomplete (with response)',
    'Incomplete (without response)',
    'Incomplete',
    'Opinion',
    'Confirmed',
    'Triaged'
)


class LaunchpadBackend(object):
    delay = 0.1

    def __init__(self):
        self.launchpad = Launchpad.login_anonymously('grepo', 'production',
                                                     settings.LP_DIR)

    def __iter__(self):
        all_languages = set(Language.objects.all().values_list('name',
                                                               flat=True))

        for project in self.launchpad.projects:

            # We are not interested in projects that do not host
            # their code on Launchpad
            if not project.getBranches()[:1]:
                continue

            # Since Launchpad allows almost *anything* in the
            # `programming language` field, we are forced to pick only
            # those repositories, which have a programming language we
            # know.
            languages = getattr(project, 'programming_language', '')
            if not languages:
                continue

            languages = re.split(r"[,;/ ]+", languages)
            languages = set(lang.strip().title() for lang in languages)

            # Hopefully the intersections will yield a non-empty list.
            languages &= all_languages

            if not languages:
                continue

            updated_at = self.get_last_updated(project)

            yield {
                'url': posixpath.join('https://launchpad.net/', project.name),
                'name': project.name,
                'summary': project.summary,
                'languages': languages,
                'score': self.calculate_score(project, updated_at),
                'created_at': project.date_created,
                'updated_at': updated_at
            }

    def calculate_score(self, project, updated_at):
        """Calculate Grepo-score for a given project."""
        issues = self.get_issues_number(project) or 1

        score = (datetime.utcnow() - updated_at.replace(tzinfo=None)).days * \
            math.exp(issues)
        return score % 365. / 365.

    def get_last_updated(self, project):
        """Get the date of the last commit to project branches"""
        updated_at = None
        for branch in project.getBranches():
            if updated_at is None:
                updated_at = branch.date_last_modified
            elif branch.date_last_modified < updated_at:
                updated_at = branch.date_last_modified
        return updated_at

    def get_issues_number(self, project, states=STATES):
        """Count all active tasks for the project"""
        num = sum(1 for task in project.searchTasks(status=states))
        return num
