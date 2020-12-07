import os.path
import tempfile
import subprocess


def tempdir(path):
    if path:
        return path
    return os.path.join(tempfile.gettempdir(), "airflow-pm2")


def exists(path):
    return os.path.exists(tempdir(path))


def makedirs(path):
    return os.makedirs(tempdir(path))


def pid(name):
    return subprocess.check_output(["pm2", "pid", name]).strip()


def start(name):
    return subprocess.check_output(["pm2", "start", name]).strip()


def restart(name):
    return subprocess.check_output(["pm2", "restart", name]).strip()


def stop(name):
    return subprocess.check_output(["pm2", "stop", name]).strip()


def reload(name):
    return subprocess.check_output(["pm2", "reload", name]).strip()
