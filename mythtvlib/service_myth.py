"""
Module: service_channel.py

Define all the MythTV classes that are part of the Channel Service
"""
import re

from mythtvlib.backend import MythTVBackend
from mythtvlib.object import MythTVClass, MythTVObjectException


CLASS_DEFINITIONS = {
    'Profile' : {
        'name'            : 'Profile',
        'service'         : 'Myth',
        'get_operation'   : 'ProfileText',
        'primary_key'     : tuple(),
        'keys'            : ['text'],
        'features'        : {
            'audio'         : 'eval',
            'branch'        : 'str',
            'channel_count' : 'int',
            'country'       : 'str',
            'database'      : 'eval',
            'grabbers'      : 'eval',
            'historical'    : 'eval',
            'language'      : 'str',
            'libapi'        : 'str',
            'logurgency'    : 'eval',
            'mythtype'      : 'int',
            'playbackprofile' : 'eval',
            'protocol'        : 'int',
            'qtversion'       : 'str',
            'recordings'      : 'eval',
            'remote'          : 'str',
            'scheduler'       : 'eval',
            'sourcecount'     : 'int',
            'storage'         : 'eval',
            'theme'           : 'str',
            'timezone'        : 'str',
            'tuners'          : 'eval',
            'tzoffset'        : 'int',
            'uuid'            : 'str',
            'version'         : 'str',
            'vtpertuner'      : 'float'
        },
    },
}



class Profile(MythTVClass):
    
    @classmethod
    def definition(cls):
        return CLASS_DEFINITIONS['Profile']

    @classmethod
    def all(cls, backend=None):
        """Answer the backend's Profile"""
        if backend is None:
            backend = MythTVBackend.default()
        profile_text = backend.service_api("Myth").service.ProfileText()
        profile = cls(text=profile_text, _backend=backend)
        return [profile]

    def get_mythtv_feature(self, feature_name):
        """Answer the requested mythtv feature name.
        
        The receivers text is mostly free-format, however the features are:
        
        - <feature_name>:
             <feature_value>
        """
        regex = re.compile('(^- {0}:)'.format(feature_name), re.MULTILINE)
        search = regex.search(self.text)
        if search is None:
            raise MythTVObjectException("Profile feature '{0}' not found".format(feature_name))
        offset = search.end() + 1
        substring = self.text[offset:]
        length = substring.find("\n")
        substring = substring[:length].strip()
        return substring

    def __getattr__(self, name):
        """Answer the requested feature"""
        feature_list = self._class_definition()['features']
        if name not in feature_list:
            raise AttributeError("'Profile' object has no attribute '{0}'".format(name))
        
        # If we got here, name is a feature
        feature_string = self.get_mythtv_feature(name)
        # Python3 doesn't have long integers
        # Remove the "L" subscript, and hopefully don't break anything else
        # Assume that any long numbers will have at least 6 digits
        feature_string = re.sub(r'([0-9]{6,})L', r'\1', feature_string)
        feature_type = feature_list[name]
        feature = eval('{0}("{1}")'.format(feature_type, feature_string))
        return feature

