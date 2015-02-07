# mythtv_cli_extensions setup
import sys
from setuptools import setup

if sys.version < "3.4.0":
    raise ValueError("mythtv_cli_extensions require python 3.4.0 or later")

setup(
    name = "mythtv_cli_extensions",
    version = "0.2.0",
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
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.4',
        'Topic :: Utilities'
    ]
)