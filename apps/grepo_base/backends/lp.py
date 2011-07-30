#!/usr/bin/env python
# -*- coding: utf-8 -*-

from launchpadlib.launchpad import Launchpad
from grepo_base.models import Repository

LAUNCHPAD_URL = 'https://launchpad.net/'

STATES = (
    'New',
    'Incomplete (with response)',
    'Incomplete (without response)',
    'Incomplete',
    'Opinion',
    'Confirmed',
    'Triaged'
)

launchpad = Launchpad.login_anonymously('grepo', 'production')

def get_repos():
    for project in launchpad.projects[:50]:
        if not hasattr(project, 'programming_language'):
            continue
        if not project.programming_language:
            continue
        yield get_project_info(project.name)

def get_project_info(name):
    project = launchpad.projects[name]
    info = {}
    info['name'] = name
    info['created_at'] = project.date_created
    info['summary'] = project.summary
    info['url'] = LAUNCHPAD_URL + name
    info['language'] = project.programming_language
    info['score'] = 0
    info['updated_at'] = get_last_updated(project)
    info['source'] = 1
    #Repository.objects.create(**info)
    return repo.language

def get_last_updated(project):
    updated_at = None
    for branch in project.getBranches():
        if updated_at is None:
            updated_at = branch.date_last_modified
        elif branch.date_last_modified < updated_at:
            updated_at = branch.date_last_modified
    return updated_at

def get_issues_number(project, states=STATES):
    num = sum(1 for bug in project.searchTasks(status=states))
    return num
