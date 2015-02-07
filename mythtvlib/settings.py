import os
import sys
from importlib import import_module

# Add the users working directory to the path so we can find a local
# settings file
sys.path.append(os.getcwd())

# HAVE_SETTINGS is true when we've successfully imported / read 
# user defined settings
HAVE_SETTINGS = False

settings_module_name = os.getenv("MYTHTV_SETTINGS", "mythtv_cli_settings")

try:
    settings = import_module(settings_module_name)
    HAVE_SETTINGS = True
except:
    settings = import_module('mythtvlib.mythtv_cli_default')
