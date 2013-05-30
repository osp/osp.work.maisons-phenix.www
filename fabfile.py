import os.path
from fabric.api import run, local, put, cd, sudo, env, prefix
from fabric.contrib.console import confirm


def download():
    """synchronizes the local db and media files from the remote ones"""
    db_path = '/srv/data_phenix/fr.stdin.phenix/db/phenix.db'
    media_path = '/srv/data_phenix/fr.stdin.phenix/documents/media'
    local('scp phenix:%s phenix/' % db_path)
    local('rsync -avz --progress --stats phenix:%s phenix/public/' % media_path)
