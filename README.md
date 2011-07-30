     ___ ___ ___ ___ ___
    | . |  _| -_| . | . |
    |_  |_| |___|  _|___|
    |___|       |_|

    -- we find, you HACK!


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

3. You're done for now ...
