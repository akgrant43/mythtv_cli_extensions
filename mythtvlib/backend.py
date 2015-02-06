"""
MythTV Backend Represntation

This is very basic at the moment, it just stores the backend location and
returns the requested service.
"""

from mythtvlib.settings import settings
from mythtvlib.services import MythTVServiceAPI



class MythTVBackend(object):
    _default = None

    def __init__(self, hostname=None, port=None):
        """Initialise the receiver.
        
        If no parameters are supplied, settings will be used.
        If settings are not defined, use defaults."""

        self.hostname = hostname
        if self.hostname is None:
            self.hostname = getattr(settings, "HOSTNAME", "localhost")
        self.port = port
        if self.port is None:
            self.port = int(getattr(settings, "PORT", 6544))
        self._service_apis = {}
        return

    @classmethod
    def default(cls, hostname=None, port=None):
        "Answer the default backend"
        if cls._default is None:
            cls._default = cls(hostname, port)
        return cls._default

    @classmethod
    def services(cls):
        return MythTVServiceAPI.services

    def service_api(self, service_name):
        api = self._service_apis.get(service_name)
        if api is None:
            api = MythTVServiceAPI(service_name, self)
            self._service_apis[service_name] = api
        return api

    def __str__(self):
        return "MythTVBackend(hostname={hostname}, port={port}".format(
                hostname=self.hostname, port=self.port)
