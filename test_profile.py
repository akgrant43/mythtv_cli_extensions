"""
Test the MythTV Profile class

These tests should run against any recent production MythTV installation (>= 0.27).

Many of the tests simply check that the attribute exists.  It would be nice
if regex's could be added that made sure the format of the response is correct.
All contributions welcome. :-)
"""

import re
import unittest
# from os.path import isdir, join, split, abspath
# from subprocess import Popen
# from tempfile import TemporaryFile

from mythtvlib.query import MythTVQuerySet

BRANCH_REs = ('fixes/0\.[0-9]{2}',)

class TestMythTVProfile(unittest.TestCase):
    
    def __init__(self, methodName='runTest'):
        super().__init__(methodName)
        self.mythtv_profile = MythTVQuerySet("Profile").all()[0]
        return

    def check_for_keys(self, feature_dict, key_list, msg):
        """Check that feature_dict contains all the keys in key_list"""
        keys = list(feature_dict.keys())
        for key in key_list:
            self.assertIn(key, keys, msg)
        return

    def test_audio(self):
        """Ensure the audio feature has the expected keys"""
        audio = self.mythtv_profile.audio
        self.check_for_keys(audio, ['passthru', 'stereopcm', 'upmixtype', 
            'volcontrol', 'defaultupmix', 'maxchannels', 'passthruoverride',
            'mixercontrol', 'audio_sys_version', 'sr_override', 'pulse',
            'passthrudevice', 'jack', 'device', 'audio_sys', 'mixerdevice'],
            "Profile.audio")
        return

    def test_branch(self):
        """Ensure the branch name looks reasonable."""
        branch = self.mythtv_profile.branch
        regexs = [re.compile(x) for x in BRANCH_REs]
        have_match = False
        for regex in regexs:
            if regex.search(branch) is not None:
                have_match = True
                break
        self.assertTrue(have_match,
            "Unrecognised branch name: {0}".format(branch))
        return

    def test_channel_count(self):
        "Ensure channel_count is returned as a positive number"
        count = self.mythtv_profile.channel_count
        self.assertGreaterEqual(count, 0, "Profile.channel_count")
        return

    def test_country(self):
        "Ensure the country is a 2 letter string"
        country = self.mythtv_profile.country
        self.assertEqual(len(country), 2, "Profile.country length")
        return

    def test_database(self):
        "Ensure the database has the expected keys"
        db = self.mythtv_profile.database
        self.check_for_keys(db, ['version', 'usedengine', 'engines', 'schema'],
                            "Profile.database")
        return

    def test_grabbers(self):
        "Ensure grabbers are returned without error"
        self.mythtv_profile.grabbers
        return

    def test_historical(self):
        "Ensure historical has the expected keys"
        historical = self.mythtv_profile.historical
        self.check_for_keys(historical, ['showcount', 'rectime', 'db_age', 'reccount'],
                            "Profile.historical")
        return

    def test_language(self):
        "Ensure the language is returned without error"
        self.mythtv_profile.language
        return

    def test_libapi(self):
        "Ensure the libapi version looks reasonable"
        libapi = self.mythtv_profile.libapi
        regex = re.compile(r'0\.[0-9]{2}\.[0-9]{8}-[0-9]{1,2}')
        self.assertIsNotNone(regex.search(libapi),
                             "Profile.libapi")
        return

    def test_logurgency(self):
        "Ensure the logurgenacy is a dictionary"
        logurgency = self.mythtv_profile.logurgency
        self.assertEqual(type(logurgency), dict,
                         "Profile.logurgency")
        return

    def test_mythtype(self):
        "Ensure the mythtype is returned without error"
        self.mythtv_profile.mythtype
        return

    def test_playbackprofile(self):
        "Ensure the playbackprofile has the expected keys"
        playbackprofile = self.mythtv_profile.playbackprofile
        self.check_for_keys(playbackprofile, ['name', 'profiles'],
                            "Profile.playbackprofile")
        return

    def test_protocol(self):
        "Ensure the protocol is returned with a reasonable value"
        protocol = self.mythtv_profile.protocol
        self.assertGreaterEqual(protocol, 77,
                                "Profile.protocol")
        return

    def test_qtversion(self):
        "Ensure the qtversion looks reasonable"
        qtversion = self.mythtv_profile.qtversion
        regex = re.compile(r'[0-9]\.[0-9]{1,2}\.[0-9]{1,2}')
        self.assertIsNotNone(regex.match(qtversion), "Profile.qtversion")
        return

    def test_recordings(self):
        "Ensure recordings have the expected keys"
        recordings = self.mythtv_profile.recordings
        self.check_for_keys(recordings, ['scheduled', 'livetv', 'expireable',
                                         'upcoming'],
                            "Profile.recordings")
        return

    def test_remote(self):
        "Ensure remote returns without error"
        self.mythtv_profile.remote
        return

    def test_scheduler(self):
        "Ensure scheduler is a dictionary"
        scheduler = self.mythtv_profile.scheduler
        self.assertEqual(type(scheduler), dict,
                         "Profile.scheduler")
        return

    def test_sourcecount(self):
        "Ensure sourcecount looks reasonable"
        sourcecount = self.mythtv_profile.sourcecount
        self.assertGreater(sourcecount, 0,
                           "Profile.sourcecount")
        return

    def test_storage(self):
        "Ensure storage has the expected keys"
        storage = self.mythtv_profile.storage
        self.check_for_keys(storage, ['rectotal', 'videofree', 'recfree',
                                      'videototal'],
                            "Profile.storage")
        return

    def test_theme(self):
        "Ensure the theme is returned without error"
        self.mythtv_profile.theme
        return

    def test_timezone(self):
        "Ensure the timezone is returned without error"
        self.mythtv_profile.timezone
        return

    def test_tuners(self):
        "Ensure tuners is a dictionary"
        tuners = self.mythtv_profile.tuners
        self.assertEqual(type(tuners), dict,
                         "Profile.tuners")
        return

    def test_tzoffset(self):
        "Ensure the tzoffset looks reasonable"
        tzoffset = self.mythtv_profile.tzoffset
        max_offset = 13*60*60
        self.assertGreaterEqual(tzoffset, 0-max_offset,
                                "Profile.tzoffset minimum")
        self.assertLessEqual(tzoffset, max_offset,
                             "Profile.tzoffset maximum")
        return

    def test_uuid(self):
        "Ensure the uuid is returned without error"
        self.mythtv_profile.uuid
        return

    def test_version(self):
        "Ensure the version looks reasonable"
        version = self.mythtv_profile.version
        regex = re.compile(r'v0\.[0-9]{2}-[0-9]{1,5}-[a-z0-9]{8}')
        self.assertIsNotNone(regex.match(version),
                             "Profile.version")
        return

    def test_vtpertuner(self):
        "Ensure the vtpertuner looks reasonable"
        vtpertuner = self.mythtv_profile.vtpertuner
        self.assertGreaterEqual(vtpertuner, 1.0,
                                "Profile.vtpertuner minimum")
        self.assertLessEqual(vtpertuner, 10.0,
                             "Profile.vtpertuner maximum")
        return
