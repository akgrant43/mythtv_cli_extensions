#
# This file contains a list of suggested tests to be performed,
# but are site specific, thus the expected results will need to be manually
# updated.
#
# Return the tests in a variable called "tests"
# tests = list(tuple(name, command, expected stdout, expected stderr))
#
tests = [
("list xmltv", "mythtv_chanmaint list xmltv",
"""CallSign             XMLTVID                                                         
-----------------------------------------
Fanda                20144.port.cz                                                   
Nova Cinema          20094.port.cz                                                   
Nova TV              20002.port.cz                                                   
Prima                20003.port.cz                                                   
Prima Cool           20129.port.cz                                                   
Prima LOVE           20137.port.cz                                                   
Prima ZOOM           20151.port.cz                                                   
TV Barrandov         20121.port.cz                                                   
Óčko                 20007.port.cz                                                   
ČT :D                20147.port.cz                                                   
ČT sport             20006.port.cz                                                   
ČT1                  20004.port.cz                                                   
ČT2                  20005.port.cz                                                   
ČT24                 20052.port.cz""", ""),

("list channels", "mythtv_chanmaint list channels",
"""Id    Src CallSign             ChanNum Name                 Visible XMLTVID              Icon URL            
----------------------------------------------------------------------------------------------------
1016  1   SMICHOV              16      SMICHOV              1                                                
1017  1   TELKA                17      TELKA                1                            telka_cz.png        
1018  1   RELAX - Pohoda       18      RELAX - Pohoda       1                            relax_pohoda_cz.png 
1019  1   REBEL                19      REBEL                1                            rebel_tv_cz.png     
1020  1   COUNTRY no 1         20      COUNTRY no 1         1                                                
1041  1   Ocko Gold            41      Ocko Gold            1                                                
1042  1   Slagr TV             42      Slagr TV             1                            slagr_tv_cz.png     
1043  1   ACTIVE               43      ACTIVE               1                            active_cz.png       
1051  1   SMICHOV              51      SMICHOV              1                                                
1052  1   TELKA                52      TELKA                1                            telka_cz.png        
1053  1   RELAX - Pohoda       53      RELAX - Pohoda       1                            relax_pohoda_cz.png 
1054  1   REBEL                54      REBEL                1                            rebel_tv_cz.png     
1055  1   COUNTRY no 1         55      COUNTRY no 1         1                                                
1058  1   SMICHOV              58      SMICHOV              1                                                
1059  1   TELKA                59      TELKA                1                            telka_cz.png        
1060  1   ZAK TV               60      ZAK TV               1                                                
1061  1   RELAX - Pohoda       61      RELAX - Pohoda       1                            relax_pohoda_cz.png 
1062  1   REBEL                62      REBEL                1                            rebel_tv_cz.png     
1063  1   COUNTRY no 1         63      COUNTRY no 1         1                                                
1261  1   CT 1 HD              261     CT 1 HD              1                            ceska_televize1_hd.png
1263  1   CT 2 HD              263     CT 2 HD              1                            ceska_televize2_hd.png
1264  1   CT:D / CT art        264     CT:D / CT art        1                            ceska_televize_d.png
1517  1   SMICHOV              517     SMICHOV              1                                                
1518  1   TELKA                518     TELKA                1                            telka_cz.png        
2026  1   Ocko Gold            1026    Ocko Gold            1                                                
2793  1   ZAK TV               1793    ZAK TV               1                                                
3817  1   RELAX - Pohoda       2817    RELAX - Pohoda       1                            relax_pohoda_cz.png 
3818  1   REBEL                2818    REBEL                1                            rebel_tv_cz.png     
4585  1   V1                   3585    V1                   1                                                
6633  1   Slagr TV             5633    Slagr TV             1                            slagr_tv_cz.png     
6634  1   COUNTRY no 1         5634    COUNTRY no 1         1                                                
6889  1   RETRO MUSIC TV       5889    RETRO MUSIC TV       1                            retro_tv_cz.png     
7145  1   KINOSVET             6145    KINOSVET             1                                                
8169  1   ACTIVE               7169    ACTIVE               1                            active_cz.png       
1021  1   NOVA                 21      NOVA                 1       20002.port.cz        nova_tv_cz.png      
1026  1   NOVA                 26      NOVA                 1       20002.port.cz        nova_tv_cz.png      
1032  1   NOVA                 32      NOVA                 1       20002.port.cz        nova_tv_cz.png      
1044  1   NOVA                 44      NOVA                 1       20002.port.cz        nova_tv_cz.png      
1513  1   NOVA                 513     NOVA                 1       20002.port.cz        nova_tv_cz.png      
1024  1   Prima                24      Prima                1       20003.port.cz        prima_tv_cz.png     
1029  1   Prima                29      Prima                1       20003.port.cz        prima_tv_cz.png     
1035  1   Prima                35      Prima                1       20003.port.cz        prima_tv_cz.png     
1047  1   Prima                47      Prima                1       20003.port.cz        prima_tv_cz.png     
1773  1   Prima                773     Prima                1       20003.port.cz        prima_tv_cz.png     
1001  1   CT 1                 1       CT 1                 1       20004.port.cz        ceska_televize1.png 
1006  1   CT 1                 6       CT 1                 1       20004.port.cz        ceska_televize1.png 
1010  1   CT 1                 10      CT 1                 1       20004.port.cz        ceska_televize1.png 
1257  1   CT 1                 257     CT 1                 1       20004.port.cz        ceska_televize1.png 
1002  1   CT 2                 2       CT 2                 1       20005.port.cz        ceska_televize2.png 
1007  1   CT 2                 7       CT 2                 1       20005.port.cz        ceska_televize2.png 
1011  1   CT 2                 11      CT 2                 1       20005.port.cz        ceska_televize2.png 
1258  1   CT 2                 258     CT 2                 1       20005.port.cz        ceska_televize2.png 
1004  1   CT sport             4       CT sport             1       20006.port.cz        ceska_televize_sport.png
1009  1   CT sport             9       CT sport             1       20006.port.cz        ceska_televize_sport.png
1013  1   CT sport             13      CT sport             1       20006.port.cz        ceska_televize_sport.png
1260  1   CT sport             260     CT sport             1       20006.port.cz        ceska_televize_sport.png
1262  1   CT sport HD          262     CT sport HD          1       20006.port.cz        ceska_televize_sport_hd.png
1040  1   Ocko                 40      Ocko                 1       20007.port.cz                            
2025  1   Ocko                 1025    Ocko                 1       20007.port.cz                            
1003  1   CT 24                3       CT 24                1       20052.port.cz        ceska_televize24.png
1008  1   CT 24                8       CT 24                1       20052.port.cz        ceska_televize24.png
1012  1   CT 24                12      CT 24                1       20052.port.cz        ceska_televize24.png
1259  1   CT 24                259     CT 24                1       20052.port.cz        ceska_televize24.png
1005  1   NOVA CINEMA          5       NOVA CINEMA          1       20094.port.cz        nova_cinema_cz.png  
1014  1   NOVA CINEMA          14      NOVA CINEMA          1       20094.port.cz        nova_cinema_cz.png  
1022  1   NOVA CINEMA          22      NOVA CINEMA          1       20094.port.cz        nova_cinema_cz.png  
1027  1   NOVA CINEMA          27      NOVA CINEMA          1       20094.port.cz        nova_cinema_cz.png  
1033  1   NOVA CINEMA          33      NOVA CINEMA          1       20094.port.cz        nova_cinema_cz.png  
1045  1   NOVA CINEMA          45      NOVA CINEMA          1       20094.port.cz        nova_cinema_cz.png  
1049  1   NOVA CINEMA          49      NOVA CINEMA          1       20094.port.cz        nova_cinema_cz.png  
1056  1   NOVA CINEMA          56      NOVA CINEMA          1       20094.port.cz        nova_cinema_cz.png  
1514  1   NOVA CINEMA          514     NOVA CINEMA          1       20094.port.cz        nova_cinema_cz.png  
1025  1   BARRANDOV TV         25      BARRANDOV TV         1       20121.port.cz        barrandov_tv.png    
1030  1   BARRANDOV TV         30      BARRANDOV TV         1       20121.port.cz        barrandov_tv.png    
1036  1   BARRANDOV TV         36      BARRANDOV TV         1       20121.port.cz        barrandov_tv.png    
1048  1   BARRANDOV TV         48      BARRANDOV TV         1       20121.port.cz        barrandov_tv.png    
3050  1   BARRANDOV TV         2050    BARRANDOV TV         1       20121.port.cz        barrandov_tv.png    
1023  1   Prima COOL           23      Prima COOL           1       20129.port.cz        prima_cool_cz.png   
1028  1   Prima COOL           28      Prima COOL           1       20129.port.cz        prima_cool_cz.png   
1034  1   Prima COOL           34      Prima COOL           1       20129.port.cz        prima_cool_cz.png   
1046  1   Prima COOL           46      Prima COOL           1       20129.port.cz        prima_cool_cz.png   
1770  1   Prima COOL           770     Prima COOL           1       20129.port.cz        prima_cool_cz.png   
1038  1   Prima LOVE           38      Prima LOVE           1       20137.port.cz        prima_love_cz.png   
1772  1   Prima LOVE           772     Prima LOVE           1       20137.port.cz        prima_love_cz.png   
1015  1   FANDA                15      FANDA                1       20144.port.cz        fanda_tv_cz.png     
1050  1   FANDA                50      FANDA                1       20144.port.cz        fanda_tv_cz.png     
1057  1   FANDA                57      FANDA                1       20144.port.cz        fanda_tv_cz.png     
1515  1   FANDA                515     FANDA                1       20144.port.cz        fanda_tv_cz.png     
1031  1   CT :D / CT art       31      CT :D / CT art       1       20147.port.cz        ceska_televize_d.png
1037  1   CT :D / CT art       37      CT :D / CT art       1       20147.port.cz        ceska_televize_d.png
1039  1   Prima ZOOM           39      Prima Zoom           1       20151.port.cz        prima_zoom_cz.png   
1774  1   Prima ZOOM           774     Prima Zoom           1       20151.port.cz        prima_zoom_cz.png""", ""),

("update V1 name to V1a", 'mythtv_cli update -y Channel CallSign "^V1\$" ChannelName "V1a"', "",
"""INFO: update Channel CallSign '^V1$' ChannelName 'V1a'
INFO: Updated: Channel(ChanId=4585) ChannelName: 'V1' => 'V1a'
INFO: Updated 1 record(s)"""),

("dump Channel 4585 V1a", "mythtv_cli dump Channel GetChannelInfo 4585",
"""(ChannelInfo){
   _serializerVersion = "1.1"
   _version = "1.06"
   ChanId = 4585
   ChanNum = "3585"
   CallSign = "V1"
   IconURL = None
   ChannelName = "V1a"
   MplexId = 0
   TransportId = 0
   ServiceId = 0
   NetworkId = 0
   ATSCMajorChan = 0
   ATSCMinorChan = 0
   Format = None
   Modulation = None
   Frequency = 0
   FrequencyId = "60"
   FrequencyTable = "default"
   FineTune = 0
   SIStandard = None
   ChanFilters = None
   SourceId = 1
   InputId = 0
   CommFree = 0
   UseEIT = False
   Visible = True
   XMLTVID = None
   DefaultAuth = None
   Programs = ""
 }""", ""),

("update V1a name to V1", 'mythtv_cli update -y Channel CallSign "^V1\$" ChannelName "V1"', "",
"""INFO: update Channel CallSign '^V1$' ChannelName 'V1'
INFO: Updated: Channel(ChanId=4585) ChannelName: 'V1a' => 'V1'
INFO: Updated 1 record(s)"""),

("dump Channel 4585 V1", "mythtv_cli dump Channel GetChannelInfo 4585",
"""(ChannelInfo){
   _serializerVersion = "1.1"
   _version = "1.06"
   ChanId = 4585
   ChanNum = "3585"
   CallSign = "V1"
   IconURL = None
   ChannelName = "V1"
   MplexId = 0
   TransportId = 0
   ServiceId = 0
   NetworkId = 0
   ATSCMajorChan = 0
   ATSCMinorChan = 0
   Format = None
   Modulation = None
   Frequency = 0
   FrequencyId = "60"
   FrequencyTable = "default"
   FineTune = 0
   SIStandard = None
   ChanFilters = None
   SourceId = 1
   InputId = 0
   CommFree = 0
   UseEIT = False
   Visible = True
   XMLTVID = None
   DefaultAuth = None
   Programs = ""
 }""", ""),

("update_xmltvids", "mythtv_chanmaint update_xmltvids", "",
"""INFO: update_xmltvids: no updates required"""),

]
