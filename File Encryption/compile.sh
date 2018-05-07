#!/bin/bash

echo "Purging files folder"
rm files/* -rf

echo "Building payload.exe"
pyinstaller src/payload.py -F
cp dist/payload files

echo "Building MyUnlock.exe"
pyinstaller src/MyUnlock.py -F
cp dist/MyUnlock files


echo "Copying orig_files to files"
cp ./orig_files/* ./files -rf
