from fabric.api import run, sudo, local, cd, env

env.hosts = ['gustav.spokehub.org']
env.user = 'anders'
nginx_hosts = ['octopus.spokehub.org']


def restart_gunicorn():
    sudo("/sbin/restart spokehub", shell=False)


def prepare_deploy():
    local("make test")


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
