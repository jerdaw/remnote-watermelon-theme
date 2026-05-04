#!/bin/bash
# Builds theme.css and zips the necessary files for RemNote upload
echo "Building theme.css..."
python3 build_theme.py
echo "Zipping theme bundle..."
# Clean old zip if it exists
rm -f remnote-watermelon-theme.zip
# Zip only the files RemNote needs for a theme package
zip remnote-watermelon-theme.zip manifest.json theme.css README.md
echo "Done! Upload remnote-watermelon-theme.zip to RemNote -> Settings -> Plugins -> Build -> Upload Theme"
