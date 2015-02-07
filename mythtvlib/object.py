import re
from copy import copy

from mythtvlib.backend import MythTVBackend

CLASS_DEFINITIONS = {
    'ChannelInfo': {
        'name'            : 'ChannelInfo',
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
        'keys' : ['ChanId', 'ChanNum', 'CallSign', 'IconURL', 'ChannelName',
                  'MplexId', 'TransportId', 'ServiceId', 'NetworkId',
                  'ATSCMajorChan' , 'ATSCMinorChan', 'Format', 'Modulation',
                  'Frequency', 'FrequencyId', 'FrequencyTable', 'FineTune',
                  'SIStandard', 'ChanFilters', 'SourceId', 'InputId',
                  'CommFree', 'UseEIT', 'Visible', 'XMLTVID', 'DefaultAuth',
                  'Programs'],
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
        if self.mythtv_class is None:
            raise MythTVObjectException("Unknown class name: {0}".format(classname))
        # _filters is a list of (field_name, field_regex, compiled_regex)
        self._filters = []
        self._records = None
        return

    def filter(self, **kwargs):
        "Add the supplied filter to the list."
        new_query = self.copy()
        attributes = self.mythtv_class.keys()
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

    def __init__(self, *args, **kwargs):
        # __setattr__ checks the value of _safe_mode and _definition,
        # to avoid a chicken-and-egg situation, bypass __setattr__
        self.__dict__['_safe_mode'] = False
        self.__dict__['_definition'] = None
        self._backend = MythTVBackend.default()
        all_attributes = []
        all_attributes.extend(self.__class__.keys())
        all_attributes.extend(['_backend', '_safe_mode', '_definition'])
        for k, v in kwargs.items():
            if k in all_attributes:
                setattr(self, k, v)
            else:
                raise TypeError('{0} is an invalid argument for {1}'.format(
                            k, self._class_definition['name']))
        return

    @classmethod
    def from_element(cls, element, backend=None):
        attributes = {}
        # Transfer all attributes from the element,
        # which is assumed to be a suds.sudsobject.Object
        for k, v in element:
            attributes[k] = v
        new_object = cls(**attributes)
        if backend is not None:
            new_object._backend = backend
        new_object._safe_mode = True
        return new_object

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
    def keys(cls):
        "Answer the attribute names of the receiver"
        return cls.definition()['keys']

    def _service_api(self):
        "Answer the receivers service api"
        return self._backend.service_api(self._class_definition()['service'])

    def _class_definition(self):
        if self._definition is None:
            self.__dict__['_definition'] = self.__class__.definition()
        return self._definition

    def __setattr__(self, name, value):
        """Ensure that we don't update an attribute that is not marked user
        modifiable.
        
        TODO: Implement a non-safe mode that allows all attributes to be
        updated"""
        if self._safe_mode:
            definition = self._class_definition()
            attributes = definition['keys']
            update_attributes = definition['update_attributes']
            if (name in attributes) and (name not in update_attributes):
                raise MythTVObjectException(("Attempted to update read-only "
                                              "attribute: {0}").format(name))
        self.__dict__[name] = value
        return

    def save(self):
        """Save the receiver on the backend.
        The receiver must have all post attributes as we cannot assume
        reasonable defaults (yet)"""
        kwargs = {}
        for obj_attr, upd_attr in self._class_definition()['post_mapping'].items():
            kwargs[upd_attr] = getattr(self, obj_attr)
        getattr(self._service_api().service, self._class_definition()['post_operation'])(**kwargs)
        return

    def __repr__(self):
        definition = self.__class__.definition()
        keys = ["{0}={1}".format(k, getattr(self, k)) for k in definition['primary_key']]
        key_string = ", ".join(keys)
        return "{name}({pkey})".format(
                name=definition['name'], 
                pkey=key_string)



class ChannelInfo(MythTVClass):

    @classmethod
    def definition(cls):
        return CLASS_DEFINITIONS['ChannelInfo']

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
        all_records = [cls.from_element(c, backend=backend) \
                       for c in cls.all_channels(backend=backend)]
        return all_records
