#!/bin/bash

# Update README.md
#
# Concatenate:
#
# 1. readme.md
# 2. mythtv_cli.py --help
# 3. mythtv_chanmaint.py --help

set -e

echo "Copying readme.md"
cp readme.md ../README.md
echo "Appending mythtv_cli help"
echo "# mythtv_cli.py help" >> ../README.md
echo "" >> ../README.md
echo "<pre>" >> ../README.md
../bin/mythtv_cli.py --help >> ../README.md
echo "</pre>" >> ../README.md
echo "" >> ../README.md
echo "Appending mythtv_chanmaint help"
echo "# mythtv_chanmaint.py help" >> ../README.md
echo "" >> ../README.md
echo "<pre>" >> ../README.md
../bin/mythtv_chanmaint.py --help >> ../README.md
echo "</pre>" >> ../README.md
echo "" >> ../README.md

