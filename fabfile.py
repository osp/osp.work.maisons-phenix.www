import os.path
from fabric.api import run, local, put, cd, sudo, env, prefix
from fabric.contrib.console import confirm


def deploy():
    """deploys to previously setup environment"""
    env.hosts = ['admin@95.142.166.47']
    env.path = '/srv/data_phenix/fr.stdin.phenix/app'
    path_activate = '/srv/data_phenix/fr.stdin.phenix/venv/bin/activate'
    path_wsgi = '/srv/data_phenix/fr.stdin.phenix/app/phenix/wsgi.py'

    with cd(env.path):
        run('git pull origin master')

        with prefix('source %s' % path_activate):
            run('python manage.py collectstatic --noinput')

    run('touch %s' % path_wsgi)


def download():
    """synchronizes the local db and media files from the remote ones"""
    db_path = '/srv/data_phenix/fr.stdin.phenix/db/phenix.db'
    media_path = '/srv/data_phenix/fr.stdin.phenix/documents/media'
    local('scp phenix:%s phenix/' % db_path)
    local('rsync -avz --progress --stats phenix:%s phenix/public/' % media_path)
