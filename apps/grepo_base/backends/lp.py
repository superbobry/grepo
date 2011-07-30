#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

def initiate_repositories_update():
    launchpad = Launchpad.login_anonymously('grepo', 'production')
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

def update_project_info(name, language_list):
    '''Create or update repository info '''
    project = launchpad.projects[name]
    repo = Repository.objects.get_or_create(url=LAUNCHPAD_URL + name)
    repo.name = name
    repo.created_at=project.date_created
    repo.summary = project.summary
    repo.score = calculate_score()
    repo.source = 1
    repo.languages = language_list
    repo.save()

def calculate_score(project):
    return 0

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
    for lang in LANGUAGES:
        if lang == 'c':
            continue
        if lang in language:
            return lang
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
    for lang in languages:
        language = guess_language(lang)
        if language:
            language_list.append(language)

    language_list = [Language.objects.get(name=l) for lang in set(language_list)]
    return language_list
