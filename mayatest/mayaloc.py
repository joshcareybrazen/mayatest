"""
"""
import os
import platform
import shutil
import tempfile
import uuid
from contextlib import contextmanager


def create_and_return(*args):
    dir_ = os.path.join(*args)
    if not os.path.exists(dir_):
        os.makedirs(dir_)
    return dir_


@contextmanager
def temp_app_dir():
    """Create a clean maya app dir to perform tests from.
    """
    maya_app_dir = os.environ['MAYA_APP_DIR']
    try:
        tmp_app_dir = create_and_return(
            tempfile.gettempdir(), 'maya_app_dir{0}'.format(str(uuid.uuid4())))
        os.environ['MAYA_APP_DIR'] = tmp_app_dir
        yield tmp_app_dir
    finally:
        shutil.rmtree(tmp_app_dir)
        os.environ['MAYA_APP_DIR'] = maya_app_dir


@contextmanager
def clean_maya_environment():
    """Contextmanager to clean maya environment variables to ensure a
    clean run.
    """
    restore = False
    with temp_app_dir():
        if all(
            [i in os.environ
             for i in ('MAYA_SCRIPT_PATH', 'MAYA_MODULE_PATH')]):
            restore = True
            script_path = os.environ['MAYA_SCRIPT_PATH']
            module_path = os.environ['MAYA_MODULE_PATH']
        try:
            os.environ['MAYA_SCRIPT_PATH'] = ''
            os.environ['MAYA_MODULE_PATH'] = ''
            yield
        finally:
            if restore:
                os.environ['MAYA_SCRIPT_PATH'] = script_path
                os.environ['MAYA_MODULE_PATH'] = module_path


def get_maya_location(version):
    """Find the location of maya installation
    """
    if 'MAYA_LOCATION' in os.environ.keys():
        return os.environ['MAYA_LOCATION']

    try:
        location = {
            'Windows': 'C:/Program Files/Autodesk/Maya{0}',
            'Darwin': '/Applications/Autodesk/maya{0}/Maya.app/Contents',
        }[platform.system()]
    except KeyError:
        location = '/usr/autodesk/maya{0}'
        if version < 2016:
            # Starting Maya 2016, the default install directory name changed.
            location += '-x64'
    return location.format(version)


def mayapy(version):
    """Find the mayapy executable path.

    """
    mayapy_executable = '{0}/bin/mayapy'.format(get_maya_location(version))
    if platform.system() == 'Windows':
        mayapy_executable += '.exe'
    return mayapy_executable
