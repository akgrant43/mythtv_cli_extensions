import os
from importlib import import_module

settings_module_name = os.getenv("MYTHTV_SETTINGS", "mythtv_cli_settings")
settings = import_module(settings_module_name)
