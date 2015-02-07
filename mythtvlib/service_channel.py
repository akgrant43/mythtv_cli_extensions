"""
Module: service_channel.py

Define all the MythTV classes that are part of the Channel Service
"""
from mythtvlib.backend import MythTVBackend
from mythtvlib.object import MythTVClass, MythTVObjectException


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
        },
}


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



