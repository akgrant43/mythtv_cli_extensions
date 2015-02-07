# Return the tests in a variable called "tests"
# tests = list(tuple(name, command, expected result))
#
tests = [
("Channel help", "mythtv_cli dump Channel help",
"""Supported Operations:
    FetchChannelsFromSource        SourceId, CardId, WaitForFinish
    GetChannelInfo                 ChanID
    GetChannelInfoList             SourceID, StartIndex, Count
    GetDDLineupList                Source, UserId, Password
    GetVideoMultiplex              MplexID
    GetVideoMultiplexList          SourceID, StartIndex, Count
    GetVideoSource                 SourceID
    GetVideoSourceList             
    GetXMLTVIdList                 SourceID""", ""),

("Myth help", "mythtv_cli dump Myth help",
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
    SendNotification               Error, Type, Message, Origin, Description, Image, Extra, ProgressText, Progress, Timeout, Fullscreen, Visibility, Priority, Address, udpPort""", ""),

]