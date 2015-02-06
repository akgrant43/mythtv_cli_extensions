"""
Test the mythtvlib.utils module
"""

import unittest
from os.path import isdir, join, split, abspath

from mythtvlib.settings import settings
from mythtvlib.utils import get_tmp_dir


class TestUtils(unittest.TestCase):
    
    def test_tmp_dir_exists(self):
        "Confirm that the test directory is correctly created"
        tmp_dir = get_tmp_dir()
        self.assertTrue(isdir(tmp_dir),
                        "tmp_dir '{0}' doesn't exist".format(tmp_dir))
        return

    def test_tmp_dir_from_settings(self):
        "Confirm that the test directory is one specified in settings"
        tmp_dir = get_tmp_dir()
        path, dir_name = split(tmp_dir)
        tmp_dirs = [abspath(x) for x in settings.TMP_DIRS]
        self.assertTrue(abspath(path) in tmp_dirs,
                        "tmp_dir '{0}' not in {1}".format(
                            path, tmp_dirs))
        self.assertTrue(dir_name == settings.TMP_DIR_NAME,
                        "tmp dir name = '{0}', expected '{1}'".format(
                            dir_name, settings.TMP_DIR_NAME))
        return
