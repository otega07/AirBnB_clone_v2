#!/usr/bin/python3
"""
fabric script based on the file 2-do_deploy_web_static.py that creates and
distributes an archive to the web servers.

execute: fab -f 3-deploy_web_static.py deploy -i ~/.ssh/id_rsa -u ubuntu
"""

from datetime import datetime
from os.path import exists, isdir
from fabric.api import env, local, put, run

env.hosts = ['52.87.255.41', '54.157.176.117']


def create_my_index():
    """Creates a my_index.html file inside web_static directory"""
    try:
        if not isdir("web_static"):
            local("mkdir web_static")
        with open("web_static/my_index.html", 'w') as f:
            f.write("<html>\n<head>\n<title>My Index</title>\n</head>\n"
                    "<body>\n<h1>Hello, this is my_index.html!</h1>\n</body>\n</html>")
        return True
    except:
        return False


def do_pack():
    """Generates a tgz archive"""
    try:
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        if not isdir("versions"):
            local("mkdir versions")
        file_name = "versions/web_static_{}.tgz".format(date)
        local("tar -cvzf {} web_static".format(file_name))
        return file_name
    except:
        return None


def do_deploy(archive_path):
    """Distributes an archive to the web servers"""
    if not exists(archive_path):
        return False
    try:
        file_n = archive_path.split("/")[-1]
        no_ext = file_n.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, '/tmp/')
        run('mkdir -p {}{}/'.format(path, no_ext))
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_n, path, no_ext))
        run('rm /tmp/{}'.format(file_n))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, no_ext))
        run('rm -rf {}{}/web_static'.format(path, no_ext))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(path, no_ext))
        return True
    except:
        return False


def deploy_locally(archive_path):
    """Deploys the archive locally"""
    try:
        file_n = archive_path.split("/")[-1]
        no_ext = file_n.split(".")[0]
        local_path = "local_releases/"
        if not isdir(local_path):
            local("mkdir -p {}".format(local_path))
        local('tar -xzf {} -C {}'.format(archive_path, local_path))
        local('rm -rf {}current'.format(local_path))
        local('ln -s {0}{1}/ {0}current'.format(local_path, no_ext))
        return True
    except:
        return False


def deploy():
    """Creates and distributes an archive to the web servers"""
    if not create_my_index():
        return False
    archive_path = do_pack()
    if archive_path is None:
        return False
    if not do_deploy(archive_path):
        return False
    return deploy_locally(archive_path)
