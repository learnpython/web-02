import os

from fabric import api


DEFAULT_BRANCH = 'master'
DEFAULT_SERVICE = 'nginx'
REPO = 'git@github.com:learnpython/web-02.git'
PROJECT_DIR = '/Users/playpauseandstop/Projects/learnpython-web-02'


def bootstrap():
    """
    Bootstrap project on remote server.
    """
    with api.cd(PROJECT_DIR):
        api.run('make bootstrap')
        api.run('make syncdb')


def commit():
    """
    Commit changed files if any.
    """
    with api.settings(warn_only=True):
        api.local('git add -i && git commit')


def deploy(branch=None):
    """
    Run full deploy process.
    """
    pre_deploy(branch)

    init()
    pull(branch)
    bootstrap()
    restart()

    post_deploy()


def init():
    """
    Initialize project dir on remote host.
    """
    parent = os.path.abspath(os.path.join(PROJECT_DIR, '..'))

    api.run('[ ! -d "{0}" ] && mkdir "{0}" || :'.format(parent))
    api.run('[ ! -d "{0}" ] && git clone {1} "{0}" || :'.
            format(PROJECT_DIR, REPO))

    with api.cd(PROJECT_DIR):
        api.run('make createdb')


def pre_deploy(branch=None):
    """
    Prepare code deployment.
    """
    test()
    commit()
    push(branch)


def post_deploy():
    """
    Code to run after successful deployment.
    """


def pull(branch=None):
    """
    Pull fresh changes on remote server.
    """
    with api.cd(PROJECT_DIR):
        api.run('git pull origin {0}'.format(branch or DEFAULT_BRANCH))


def push(branch=None):
    """
    Push commited files to remote repo.
    """
    api.local('git push origin {0}'.format(branch or DEFAULT_BRANCH))


def restart(service=None):
    """
    Restart service on remote server.
    """
    api.sudo('service {0} restart'.format(service or DEFAULT_SERVICE))


def syncdb():
    """
    Run syncdb and migrate commands on remote server.
    """
    with api.cd(PROJECT_DIR):
        api.run('make syncdb')


def test():
    """
    Run project tests.
    """
    api.local('make test')
