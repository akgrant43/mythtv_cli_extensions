import re
from copy import copy

from mythtvlib.backend import MythTVBackend

CLASS_DEFINITIONS = {
    'Channel': {
        'name'            : 'Channel',
        'service'         : 'Channel',
        'get_operation'   : 'GetChannelInfo',
        'primary_key'     : ('ChanId',),
        'post_operation'  : 'UpdateDBChannel',
        'post_mapping'    : {
            'ChanId' : 'ChannelID',
            'ChanNum' : 'ChannelNumber',
            'CallSign' : 'CallSign',
            'IconURL' : 'Icon',
            'ChannelName' : 'ChannelName',
            'MplexId' : 'MplexID',
            'ServiceId' : 'ServiceID',
            'SourceId' : 'SourceID',
            'ATSCMajorChan' : 'ATSCMajorChannel',
            'ATSCMinorChan' : 'ATSCMinorChannel',
            'UseEIT' : 'UseEIT',
            'Visible' : 'visible',
            'FrequencyId' : 'FrequencyID',
            'Format' : 'Format',
            'XMLTVID' : 'XMLTVID',
            'DefaultAuth' : 'DefaultAuthority'
            },
        'update_attributes' : ['ChanNum', 'CallSign', 'ChannelName',
                            'IconURL', 'Visible', 'XMLTVID']
        }
}


class MythTVObjectException(Exception):
    pass


class MythTVQuerySet(object):
    """Provide a django like interface for filtering MythTV objects."""
    
    def __init__(self, classname):
        self.mythtv_class = MythTVClass.classname(classname)
        # _filters is a list of (field_name, field_regex, compiled_regex)
        self._filters = []
        self._records = None
        return

    def filter(self, **kwargs):
        "Add the supplied filter to the list."
        new_query = self.copy()
        attributes = self.mythtv_class.attrib()
        for k, v in kwargs.items():
            if k not in attributes:
                raise MythTVObjectException(("Attempt to filter on" 
                                    "non-existant attribute: {0}").format(k))
            new_query._filters.append((k, v, re.compile(v)))
        if self._records is not None and len(self._records) > 0:
            self._apply_filters()
        return new_query

    def _apply_filters(self):
        """Apply the receivers filters to the records"""
        if self._records is None:
            self._records = self.mythtv_class.all()
        # TODO: This can probably be optimised in some way
        if len(self._filters) > 0:
            filtered_records = []
            for rec in self._records:
                for f in self._filters:
                    if f[2].search(getattr(rec, f[0])):
                        filtered_records.append(rec)
            self._records = filtered_records
        return

    def all(self):
        """Answer all the records in a copy of the receiver"""
        self._apply_filters()
        return self._records

    def copy(self):
        """Answer a copy of the receiver.
        If _records are not None, copy the record list"""
        new_copy = copy(self)
        if new_copy._records is not None:
            new_copy._records = copy(new_copy._records)
        return new_copy




class MythTVClass(object):
    """Abstract superclass to provide an object representation of a
    MythTV backend web service object"""
    _local_vars = ["_backend", "_element", "_local_vars",
                   "_definition"]

    def __init__(self, element, backend=None):
        self._element = element
        self._definition = None
        if backend is None:
            self._backend = MythTVBackend.default()
        else:
            self._backend = backend
        return

    @classmethod
    def classname(cls, name):
        "Answer the appropriate subclass"
        subclasses = cls.__subclasses__()
        subclass = None
        for cl in subclasses:
            if name == cl.__name__:
                subclass = cl
                break
        return subclass

    @classmethod
    def definition(cls):
        "Answer the receivers definition"
        raise MythTVObjectException("Subclass responsibility")

    @classmethod
    def attrib(cls):
        "Answer the attribute names of the receiver"
        return cls.definition()['post_mapping'].keys()

    def _service_api(self):
        "Answer the receivers service api"
        return self._backend.service_api(self._class_definition()['service'])

    def _class_definition(self):
        if self._definition is None:
            self._definition = self.__class__.definition()
        return self._definition

    def __getattr__(self, name):
        "Simply pass on any unknown attributes to the element"
        return getattr(self._element, name)

    def __setattr__(self, name, value):
        "Simply pass on any unknown attributes to the element"
        if name in self._local_vars:
            # _element is stored locally
            self.__dict__[name] = value
        else:
            definition = self._class_definition()
            if name not in definition['post_mapping'].keys():
                raise MythTVObjectException(("Attempted to update unknown "
                                             "attribute: {0}").format(name))
            elif name not in definition['update_attributes']:
                raise MythTVObjectException(("Attempted to update read-only "
                                              "attribute: {0}").format(name))
            setattr(self._element, name, value)
        return

    def save(self):
        """Save the receiver on the backend"""
        kwargs = {}
        for obj_attr, upd_attr in self._class_definition()['post_mapping'].items():
            kwargs[upd_attr] = self._element[obj_attr]
        getattr(self._service_api().service, self._class_definition()['post_operation'])(**kwargs)
        return

    def __repr__(self):
        definition = self.__class__.definition()
        keys = ["{0}={1}".format(k, getattr(self, k)) for k in definition['primary_key']]
        key_string = ", ".join(keys)
        return "{name}({pkey})".format(
                name=definition['name'], 
                pkey=key_string)



class MythTVChannel(MythTVClass):

    @classmethod
    def definition(cls):
        return CLASS_DEFINITIONS['Channel']

    @classmethod
    def videosources(cls, backend=None):
        """Iterate over all videosources in the backend"""
        if backend is None:
            backend = MythTVBackend.default()
        video_services = backend.service_api("Channel").service.GetVideoSourceList()
        for vss in video_services.VideoSources:
            yield vss[1]
        return

    @classmethod
    def channels(cls, videosource_id, backend=None):
        """Iterate over all channels in the specified videosource id"""
        if backend is None:
            backend = MythTVBackend.default()
        channels = backend.service_api("Channel").service.GetChannelInfoList(videosource_id)
        # channels is a ChannelInfoList
        # channels.ChannelInfos is ArrayOfChannelInfo,
        # which is a an array like object with one entry,
        # a list of ChannelInfo
        for channel in channels.ChannelInfos[0]:
            yield channel
        return        

    @classmethod
    def all_channels(cls, backend=None):
        "Iterate over all channels, i.e. over all videosources"
        for vss in cls.videosources(backend=backend):
            for vs in vss:
                for channel in cls.channels(vs.Id, backend=backend):
                    yield channel
        return

    @classmethod
    def all(cls, backend=None):
        """Answer all the receivers records fetched from the backend"""
        all_records = [cls(c, backend) for c in \
                       cls.all_channels(backend=backend)]
        return all_records
