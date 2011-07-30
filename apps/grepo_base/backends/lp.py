#!/usr/bin/env python
# -*- coding: utf-8 -*-

import string
from launchpadlib.launchpad import Launchpad
from django.conf import settings
from grepo_base.models import Repository, Language

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

LANGUAGES = Language.objects.all().values_list('name', flat=True)

launchpad = Launchpad.login_anonymously('grepo', 'production')

def get_repos():
    for project in launchpad.projects[:100]:
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
    info['score'] = 0
    info['source'] = 1
    repo = Repository.objects.create(**info)
    repo.languages = language_list
    repo.save()

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
    '''Count all active tasks for the project
    
    This is going to affect grepo-score supposedly.
    '''
    num = sum(1 for task in project.searchTasks(status=states))
    return num

def guess_language(language):
    '''Try to guess a proper language name based on user input'''
    language = language.strip().title()
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
    
    language_list = [Language.objects.get(name=l) for l in set(language_list)]
    return language_list
