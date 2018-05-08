#!/bin/bash

echo "Purging files folder"
rm files/* -rf

echo "Building payload.exe"
pyinstaller src/payload.py -F
cp dist/payload files

echo "Building MyUnlock.exe"
pyinstaller src/MyUnlock.py -F
cp dist/MyUnlock files

cp dist/payload* ../TLS_Server/payload
cp dist/MyUnlock* ../TLS_Server/MyUnlock

chmod 774 ../TLS_Server/payload/*
chmod 774 ../TLS_Server/MyUnlock/*


echo "Copying orig_files to files"
cp ./orig_files/* ./files -rf
