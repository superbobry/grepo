#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    grepo_base.backends.lp
    ~~~~~~~~~~~~~~~~~

    Launchpad backend for `grepo`.
'''

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

class LaunchpadBackend(object):
    def __init__(self):
        self.launchpad = Launchpad.login_anonymously('grepo', 'production')
    
    def __iter__(self):
        for project in self.launchpad.projects:
            # We only add projects with recognizable
            # programming languages
            if not hasattr(project, 'programming_language'):
                continue
            if not project.programming_language:
                continue
            language_list = self.get_project_languages(project.programming_language)
            if not language_list:
                continue
            yield self.get_project_info(project.name, language_list)
    
    def get_project_info(self, name, language_list):
        project = self.launchpad.projects[name]
        return {
            'url': LAUNCHPAD_URL + name,
            'name': name,
            'created_at': project.date_created,
            'summary': project.summary,
            'score': self.calculate_score(project),
            'languages': language_list,
        }
    
    def calculate_score(self, project):
        '''Calculate Grepo-score'''
        return 0
    
    def get_last_updated(self, project):
        '''Date of the last commit to project branches'''
        updated_at = None
        for branch in project.getBranches():
            if updated_at is None:
                updated_at = branch.date_last_modified
            elif branch.date_last_modified < updated_at:
                updated_at = branch.date_last_modified
        return updated_at
    
    def get_issues_number(self, project, states=STATES):
        '''Count all active tasks for the project
        
        This is going to affect Grepo-score supposedly.
        '''
        num = sum(1 for task in project.searchTasks(status=states))
        return num
    
    def guess_language(self, language):
        '''Try to guess a proper language name based on user input'''
        language = language.strip().title()
        if language in LANGUAGES:
            return language
        for lang in LANGUAGES:
            if lang == 'c':
                continue
            if lang in language:
                return lang
        return None
    
    def get_project_languages(self, language_string):
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
            language = self.guess_language(lang)
            if language:
                language_list.append(language)
        
        language_list = [Language.objects.get(name=lang) for lang in set(language_list)]
        return language_list
    
