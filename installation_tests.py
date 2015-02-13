# Return the tests in a variable called "tests"
# tests = list(dict(name, command, expected_status, expected_stdout,
#                   expected_stderr, post_script))
#

# pre_script will be executed prior to tests,
# post_script after
# Both are python3 scripts
pre_script = """
"""

post_script = """
"""

tests = [
{
    'name' : "Channel help",
    'command' : "mythtv_cli dump Channel help",
    'expected_stdout' :
"""Supported Operations:
    FetchChannelsFromSource        SourceId, CardId, WaitForFinish
    GetChannelInfo                 ChanID
    GetChannelInfoList             SourceID, StartIndex, Count
    GetDDLineupList                Source, UserId, Password
    GetVideoMultiplex              MplexID
    GetVideoMultiplexList          SourceID, StartIndex, Count
    GetVideoSource                 SourceID
    GetVideoSourceList             
    GetXMLTVIdList                 SourceID"""
},

{
    'name' : "Myth help",
    'command' : "mythtv_cli dump Myth help",
    'expected_stdout' :
"""Supported Operations:
    GetConnectionInfo              Pin
    GetHostName                    
    GetHosts                       
    GetKeys                        
    GetLogs                        HostName, Application, PID, TID, Thread, Filename, Line, Function, FromTime, ToTime, Level, MsgContains
    GetSetting                     HostName, Key, Default
    GetStorageGroupDirs            GroupName, HostName
    GetTimeZone                    
    ProfileText                    
    ProfileURL                     
    ProfileUpdated                 
    SendMessage                    Message, Address, udpPort, Timeout
    SendNotification               Error, Type, Message, Origin, Description, Image, Extra, ProgressText, Progress, Timeout, Fullscreen, Visibility, Priority, Address, udpPort""",
},

{
    'name' : "ChanMaint too many params",
    'command' : "mythtv_chanmaint list xmltv badparam",
    'expected_status' : 1,
    'expected_stderr' :
        "CRITICAL: Expecting only 1 parameter, got: ['xmltv', 'badparam']",
},

]