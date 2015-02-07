# mythtv_cli_extensions setup
from setuptools import setup

setup(
    name = "mythtv_cli_extensions",
    version = "0.1.0",
    description = "MythTV CLI Extensions",
    author = "Alistair Grant",
    author_email = "akgrant0710@gmail.com",
    url = "http://random0musings.blogspot.com/",
    long_description = open("README.txt").read(),
    packages = ["mythtvlib"],
    install_requires = ['suds-jurko'],
    entry_points = {
        'console_scripts' : [
            'mythtv_cli = mythtvlib.mythtv_cli:main',
            'mythtv_chanmaint = mythtvlib.mythtv_chanmaint:main',
        ],
    },
)