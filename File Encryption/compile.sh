#!/bin/bash

echo "Building payload.exe"
pyinstaller src/payload.py -F
cp dist/payload files

echo "Removing existing pem files"
rm files/*pem -rf

echo "Building MyUnlock.exe"
pyinstaller src/MyUnlock.py -F
cp dist/MyUnlock files
