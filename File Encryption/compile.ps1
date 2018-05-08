.\venv\Scripts\Activate.ps1

echo "Purging files folder"
rm files/* -Recurse -Force

echo "Building payload.exe"
pyinstaller src/payload.py -F
cp dist/payload.exe files

echo "Building MyUnlock.exe"
pyinstaller src/MyUnlock.py -F
cp dist/MyUnlock.exe files


echo "Copying orig_files to files"
cp ./orig_files/* ./files -Recurse -Force

Read-Host -Prompt "Press Enter to exit"