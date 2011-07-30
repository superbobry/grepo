#!/usr/bin/env python
# -*- coding: utf-8 -*-

import string
from launchpadlib.launchpad import Launchpad
from django.conf import settings
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

LANGUAGES = set([
    'python',
    'c++',
    'java',
    'php',
    'ruby',
    'c',
    'perl',
    'c#',
    'bash',
    'lisp',
    'vala',
    'javascript',
    'lua',
    'pascal',
    'ada',
    'ocaml',
    'delphi',
    'erlang'
])

launchpad = Launchpad.login_anonymously('grepo', 'production')

def get_repos():
    for project in launchpad.projects[:1000]:
        # We only add projects with recognizable
        # programming languages
        if not hasattr(project, 'programming_language'):
            continue
        if not project.programming_language:
            continue
        language_list = get_project_languages(project.programming_language)
        if not language_list:
            continue
        yield get_project_info(project.name, language_list)

def get_project_info(name, language_list):
    project = launchpad.projects[name]
    info = {}
    info['name'] = name
    info['created_at'] = project.date_created
    info['summary'] = project.summary
    info['url'] = LAUNCHPAD_URL + name
    info['language'] = language_list
    info['score'] = 0
    info['source'] = 1
    #Repository.objects.create(**info)

def get_last_updated(project):
    '''Date of the last commit to project branches'''
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

def guess_language(language):
    language = language.strip().lower()
    if language in LANGUAGES:
        return language
    # Try non-exact match, doesn't work for C :(
    for l in LANGUAGES:
        if l == 'c':
            continue
        if l in language:
            return l
    return None

def get_project_languages(language_string):
    '''Try to get the list of programming languages for the project'''

    languages = language_string.split(r',')
    if len(languages) == 1:
        languages = language_string.split(r';')
    if len(languages) == 1:
        languages = language_string.split(r'/')
    if len(languages) == 1:
        languages = language_string.split(r' ')

    language_list = []
    for l in languages:
        language = guess_language(l)
        if language:
            language_list.append(language)

    return set(language_list)
