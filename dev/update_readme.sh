#!/bin/bash

# Update README.md
#
# Concatenate:
#
# 1. readme.md
# 2. mythtv_cli --help
# 3. mythtv_chanmaint --help

set -e

echo "Copying readme.md"
cp readme.md ../README.md
echo "Appending mythtv_cli help"
echo "# mythtv_cli help" >> ../README.md
echo "" >> ../README.md
echo "\`\`\`" >> ../README.md
mythtv_cli --help | sed "s/</\&lt;/g" | sed "s/>/\&gt;/g" >> ../README.md
echo "\`\`\`" >> ../README.md
echo "" >> ../README.md
echo "Appending mythtv_chanmaint help"
echo "# mythtv_chanmaint help" | sed "s/</\&lt;/g" | sed "s/>/\&gt;/g" >> ../README.md
echo "" >> ../README.md
echo "\`\`\`" >> ../README.md
mythtv_chanmaint --help >> ../README.md
echo "\`\`\`" >> ../README.md
echo "" >> ../README.md

