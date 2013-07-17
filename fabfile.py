import os

from fabric import api


DEFAULT_BRANCH = 'master'
REPO = 'git@github.com:learnpython/web-02.git'
PROJECT_DIR = '/srv/projects/learnpython/web-02'


def bootstrap():
    """
    Bootstrap project on remote server.
    """
    with api.cd(PROJECT_DIR):
        api.run('make bootstrap')


def commit():
    """
    Commit changed files if any.
    """
    api.local('git add -p && git commit')


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
