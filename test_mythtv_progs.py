"""
Test the mythtv_cli.py command line
"""

import unittest
from os.path import isdir, join, split, abspath
from subprocess import Popen
from tempfile import TemporaryFile

from fuzzywuzzy import fuzz

from mythtvlib import __VERSION__
from mythtvlib.settings import settings

class TestMythTVCommands(unittest.TestCase):

    def setUp(self):
        self.open_temp_files()
        return

    def open_temp_files(self):
        self.stdoutfp = TemporaryFile()
        self.stderrfp = TemporaryFile()
        return

    def tearDown(self):
        self.close_temp_files()
        return

    def close_temp_files(self):
        self.stdoutfp.close()
        self.stderrfp.close()
        return

    def run_command(self, command):
        """Run the supplied command in a shell
        with output to the temporary files"""
        self.proc = Popen(command,
                          shell=True,
                          stdout=self.stdoutfp,
                          stderr=self.stderrfp)
        self.proc.wait()
        self.stdoutfp.seek(0)
        self.stderrfp.seek(0)
        self.stdout = self.stdoutfp.read().decode('utf-8').strip()
        self.stderr = self.stderrfp.read().decode('utf-8').strip()
        self.assertEqual(self.proc.returncode, 0,
            "Process exited with code: {0}, stderr: '{1}'".format(
                self.proc.returncode, self.stderr))
        return

    def test_cli_version(self):
        """Check that the mythtv_cli.py command returns the expected version
        string"""
        cmd = "bin/mythtv_cli.py --version"
        self.run_command(cmd)
        expected = 'mythtv_cli.py version ' + __VERSION__
        self.assertEqual(self.stdout, expected,
                         "Expected version '{0}', got '{1}'".format(
                            expected, self.stdout))
        self.assertEqual(len(self.stderr), 0,
                         "Expected empty stderr, got: '{0}'".format(self.stderr))
        return

    def test_chanmaint_version(self):
        """Check that the mythtv_chanmaint.py command returns the expected
        version string"""
        cmd = "bin/mythtv_chanmaint.py --version"
        self.run_command(cmd)
        expected = 'mythtv_chanmaint.py version ' + __VERSION__
        self.assertEqual(self.stdout, expected,
                         "Expected version '{0}', got '{1}'".format(
                            expected, self.stdout))
        self.assertEqual(len(self.stderr), 0,
                         "Expected empty stderr, got: '{0}'".format(self.stderr))
        return

    def test_cli_help(self):
        "Check that --help produces a reasonable amount of text"
        cmd = "bin/mythtv_cli.py --help"
        self.run_command(cmd)
        self.assertTrue(len(self.stdout) > 1000,
                        "Not much help from mythtv_cli.py")
        return

    def test_chainmaint_help(self):
        "Check that --help produces a reasonable amount of text"
        cmd = "bin/mythtv_chanmaint.py --help"
        self.run_command(cmd)
        self.assertTrue(len(self.stdout) > 3000,
                        "Not much help from mythtv_chanmaint.py")
        return

    def run_test_file(self, filename):
        """Run the supplied command line test file.
        
        The file is a list of tuples: (command, expected stdout)"""
        with open(filename) as fp:
            fcontents = fp.read()
        file_globals = {}
        file_locals = {}
        exec(fcontents, file_globals, file_locals)
        # file_locals should contain a list of 'tests'
        for test in file_locals['tests']:
            self.check_command(test[0], test[1], test[2], test[3])
            # Since we're re-using the temp file within a single test
            # we have to manually close (thus deleting) and re-open
            # the temporary files
            self.close_temp_files()
            self.open_temp_files()
        return

    def check_command(self, name, cmd, stdout, stderr):
        """Run the supplied command and confirm that stdout and stderr match
        
        The attribute order can change between runs, use sorted token matching
        to compare the outputs"""
        self.run_command(cmd)
        if len(stdout) == 0 and len(self.stdout) == 0:
            score = 100
        else:
            score = fuzz.token_sort_ratio(self.stdout, stdout)
        if score != 100:
            import pdb; pdb.set_trace()
        self.assertEqual(score, 100,
                         "Name: {0} - stdout".format(name))
        if len(stderr) == 0 and len(self.stderr) == 0:
            score = 100
        else:
            score = fuzz.token_sort_ratio(self.stderr, stderr)
        if score != 100:
            import pdb; pdb.set_trace()
        self.assertEqual(score, 100,
                         "Name: {0} - stderr".format(name))
        return

    def test_installation_common(self):
        """Run the tests in installation_tests.py
        
        These should succeed on all
        MythTV installations (of the appropriate version)"""
        self.run_test_file('installation_tests.py')
        return

    def test_site_specific(self):
        """Run the tests in site_tests.py
        
        These will need to be defined for each test environment"""
        self.run_test_file('site_tests.py')
        return

    def test_backend_version(self):
        """Check that the backend version is supported.
        Currently only 0.27"""
        self.run_command('bin/mythtv_cli.py dump Myth ProfileText | grep -A 1 "\- version"')
        self.assertTrue('v0.27' in self.stdout,
                        "Couldn't find expected version in: '{0}'".format(
                            self.stdout))
        return
