from mythtvlib.services import MythTVService

CLASS_DEFINITIONS = {
    'Channel': {
        'get_operation'   : 'GetChannelInfo',
        'get_keyname'     : 'ChanId',
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
            }
        }
}


class MythTVObject(object):
    """Abstract superclass for MythTV classes"""
    _local_vars = ["classname", "id", "_definition", "_element", "_service",
                   "_local_vars"]

    def __init__(self, classname, eid, hostname='localhost', port=6544):
        self.classname = classname
        self.id = eid
        self._definition = CLASS_DEFINITIONS[classname]
        self._service = MythTVService(classname, hostname, port)
        # self._element must be set by the subclass
        self._element = getattr(self._service.service,
                                self._definition['get_operation'])(*eid)
        return

    def __getattr__(self, name):
        "Simply pass on any unknown attributes to the element"
        return getattr(self._element, name)

    def __setattr__(self, name, value):
        "Simply pass on any unknown attributes to the element"
        if name in self._local_vars:
            # _element is stored locally
            self.__dict__[name] = value
        else:
            setattr(self._element, name, value)
        return

    def save(self):
        """Save the receiver on the backend"""
        kwargs = {}
        for obj_attr, upd_attr in self._definition['post_mapping'].items():
            kwargs[upd_attr] = self._element[obj_attr]
        getattr(self._service.service, self._definition['post_operation'])(**kwargs)
        return
