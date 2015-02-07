#!/bin/bash
#
# Update the mythtv_cli_extensions package:
#
# * Update README.md
# * Regenerate README.txt
# * check packaging
# * Generate package

set -e
set -v
cd dev
./update_readme.sh
cd ..
pandoc --to=plain README.md > README.txt
python3 setup.py check
python3 setup.py sdist

