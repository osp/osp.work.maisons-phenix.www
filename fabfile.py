import os.path
from fabric.contrib.project import rsync_project
from fabric.context_managers import lcd
from fabric.api import run, local, put, cd, sudo, env
from fabric.contrib.console import confirm
import tempfile


#def production():
    #env.hosts = ['stdin@mozzarella.stdin.fr']
    #env.path = '/home/stdin/www/bla/'


#def fix_permissions():
    ## fixes permission issues
    #sudo('chown -R %s:www-data %s' % (env.user, env.path))
    #sudo('chmod -R g+w %sesadgv' % env.path)
    #sudo('apache2ctl graceful')


def deploy(treeish='HEAD'):
    pass
