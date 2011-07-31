     ___ ___ ___ ___ ___
    | . |  _| -_| . | . |
    |_  |_| |___|  _|___|
    |___|       |_|

    -- we find, you HACK!


[grepo](http://grepo.ep.io) is a DjangoDash2011 project, helping people
find Open Source projects in need.


Installation
------------

1. First install all `grepo` dependencies with `pip`:

        $ pip install -r REQUIREMENTS.txt

2. Sync the database and migrate `grepo` applications using South:

        $ ./manage.py syncdb

        Syncing...
        Creating table auth_permission
        Creating table auth_group_permissions
        Creating table auth_group
        ...

        $ ./manage.py migrate

3. You're almost done, now run `celeryd` and Django built-in server and
  fire database update:

       $ ./manage.py celeryd -B
       $ ./manage.py runserver
       $ ./manage.py celeryctl apply grepo_base.tasks.update_world


Usage
-----

    $ grepo --help
    grepo -l LANGUAGE [-o] RESULTS [KEYWORDS]

    (no help text available)

    options:

     -l --language  programming language you want to grepo for
     -o --only      maximum number of projects to look up (default: 20)
     -h --help      show help
