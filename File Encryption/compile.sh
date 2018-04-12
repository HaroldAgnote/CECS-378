#!/bin/bash

pyinstaller payload.py -F
cp dist/payload files
