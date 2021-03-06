from fabric.api import run, sudo, local, cd, env

env.hosts = ['188.166.52.181']
env.user = 'anders'
nginx_hosts = ['10.133.47.51']


def restart_gunicorn():
    sudo("systemctl stop spokehub || true", shell=False)
    sudo("systemctl start spokehub", shell=False)


def prepare_deploy():
    local("make test")


def sentry():
    url = ("https://sentry.io/api/hooks/release/builtin/"
           "305941/a1598af8c2efee2a4fd205aff2386cad5b25e"
           "451c31f2fbfc89b5f85b8d0232b/")
    local("""COMMIT=$(git log -n 1 --pretty=format:'%%H') && curl %s \
    -X POST \
    -H 'Content-Type: application/json' \
    -d "{\\\"version\\\": \\\"$COMMIT\\\"}" """ % (url))


def deploy():
    code_dir = "/var/www/spokehub/spokehub"
    with cd(code_dir):
        run("git pull origin master")
        run("make migrate")
        run("make collectstatic")
        run("make compress")
        for n in nginx_hosts:
            run(("rsync -avp media/ "
                 "%s:/var/www/spokehub/spokehub/media/") % n)
    restart_gunicorn()
    sentry()
