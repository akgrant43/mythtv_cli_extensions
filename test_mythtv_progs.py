"""
Test the mythtv_cli & mythtv_chanmaint command lines
"""

import difflib
import unittest
from subprocess import Popen
from tempfile import TemporaryFile

from fuzzywuzzy import fuzz

from mythtvlib import __VERSION__

class TestMythTVCommandsError(Exception):
    pass



def print_string_diff(s1, s2):
    for i,s in enumerate(difflib.ndiff(s1, s2)):
        if s[0]==' ': continue
        elif s[0]=='-':
            print(u'Delete "{}" from position {}'.format(s[-1],i))
        elif s[0]=='+':
            print(u'Add "{}" to position {}'.format(s[-1],i))    
    return



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

    def run_command(self, command, name, status):
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
        self.assertEqual(self.proc.returncode, status,
            "run_command: Name: {0}, stderr: '{1}'".format(
                name, self.stderr))
        return

    def test_cli_version(self):
        """Check that the mythtv_cli command returns the expected version
        string"""
        cmd = "mythtv_cli --version"
        self.run_command(cmd, "test_cli_version", 0)
        expected = 'mythtv_cli version ' + __VERSION__
        self.assertEqual(self.stdout, expected,
                         "Expected version '{0}', got '{1}'".format(
                            expected, self.stdout))
        self.assertEqual(len(self.stderr), 0,
                         "Expected empty stderr, got: '{0}'".format(self.stderr))
        return

    def test_chanmaint_version(self):
        """Check that the mythtv_chanmaint command returns the expected
        version string"""
        cmd = "mythtv_chanmaint --version"
        self.run_command(cmd, "test_chanmaint_version", 0)
        expected = 'mythtv_chanmaint version ' + __VERSION__
        self.assertEqual(self.stdout, expected,
                         "Expected version '{0}', got '{1}'".format(
                            expected, self.stdout))
        self.assertEqual(len(self.stderr), 0,
                         "Expected empty stderr, got: '{0}'".format(self.stderr))
        return

    def test_cli_help(self):
        "Check that --help produces a reasonable amount of text"
        cmd = "mythtv_cli --help"
        self.run_command(cmd, "test_cli_help", 0)
        self.assertTrue(len(self.stdout) > 1000,
                        "Not much help from mythtv_cli")
        return

    def test_chainmaint_help(self):
        "Check that --help produces a reasonable amount of text"
        cmd = "mythtv_chanmaint --help"
        self.run_command(cmd, "test_chanmaint_help", 0)
        self.assertTrue(len(self.stdout) > 3000,
                        "Not much help from mythtv_chanmaint")
        return

    def run_test_file(self, filename):
        """Run the supplied command line test file.

        The file is a list of dicts:
            (name, command, expected_status, expected_stdout,
             expected_stderr, post_script))"""
        with open(filename) as fp:
            fcontents = fp.read()
        file_globals = {}
        file_locals = {}
        exec(fcontents, file_globals, file_locals)
        # pre_script is optional and executed prior to the tests
        if len(file_locals['pre_script'].strip()) > 0:
            exec(file_locals['pre_script'], file_globals, file_locals)
        # file_locals should contain a list of 'tests'
        for test in file_locals['tests']:
            # Check that the test only contains the expected keys
            for k in test.keys():
                if k not in ['name', 'command', 'expected_status',
                             'expected_stdout', 'expected_stderr',
                             'post_script']:
                    raise TestMythTVCommandsError(
                        "Unexpected test key: {0}".format(k)) 
            name = test['name']
            command = test['command']
            expected_status = test.get('expected_status', 0)
            expected_stdout = test.get('expected_stdout', "")
            expected_stderr = test.get('expected_stderr', "")
            post_script = test.get('post_script', "")
            self.check_command(name, command, expected_status, expected_stdout, expected_stderr)
            # Since we're re-using the temp file within a single test
            # we have to manually close (thus deleting) and re-open
            # the temporary files
            self.close_temp_files()
            self.open_temp_files()
            if len(post_script) > 0:
                "Run the specified script"
                exec(post_script, file_globals, file_locals)
        # post_script is optional and executed after the tests
        if len(file_locals['post_script'].strip()) > 0:
            exec(file_locals['post_script'], file_globals, file_locals)
        print("Executed {count} tests from {filename}".format(
            count=len(file_locals['tests']),
            filename=filename))
        return

    def check_command(self, name, cmd, status, stdout, stderr):
        """Run the supplied command and confirm that stdout and stderr match

        The attribute order can change between runs, use sorted token matching
        to compare the outputs"""
        self.run_command(cmd, name, status)
        if len(stdout) == 0 and len(self.stdout) == 0:
            score = 100
        else:
            score = fuzz.token_sort_ratio(self.stdout, stdout)
        if score != 100:
            print("{0} - stdout mismatch".format(name))
            print("="*132)
            print("Expected:")
            print(stdout)
            print("-"*132)
            print("Got:")
            print(self.stdout)
            print("-"*132)
            print_string_diff(stdout, self.stdout)
            print("-"*132)
        self.assertEqual(score, 100,
                         "Name: {0} - stdout".format(name))
        if len(stderr) == 0 and len(self.stderr) == 0:
            score = 100
        else:
            score = fuzz.token_sort_ratio(self.stderr, stderr)
        if score != 100:
            print("{0} - stderr mismatch".format(name))
            print("="*132)
            print("Expected:")
            print(stderr)
            print("-"*132)
            print("Got:")
            print(self.stderr)
            print("-"*132)
            print_string_diff(stderr, self.stderr)
            print("-"*132)
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
        self.run_command(
            'mythtv_cli dump Myth ProfileText | grep -A 1 "\- version"',
            "test_backend_version",
            0)
        self.assertTrue('v0.27' in self.stdout,
                        "Couldn't find expected version in: '{0}'".format(
                            self.stdout))
        return
