@echo off
:: Set variables for download URL and target directory
set URL=https://storage.googleapis.com/chrome-for-testing-public/130.0.6723.58/win64/chrome-win64.zip
set TARGET_DIR=chrome-win64

:: Check if the target directory exists, create it if not
if not exist "%TARGET_DIR%" (
    echo Creating target directory: %TARGET_DIR%
    mkdir "%TARGET_DIR%"
)

:: Download the Chrome zip file using curl
echo Downloading Chrome...
curl -L -o "%TARGET_DIR%\chrome-win64.zip" %URL%

:: Check if the download was successful
if exist "%TARGET_DIR%\chrome-win64.zip" (
    echo Download completed successfully.
) else (
    echo Download failed!
    exit /b 1
)

:: Extract the downloaded zip file to the target directory using PowerShell
echo Extracting Chrome to %TARGET_DIR%...
powershell -Command "Expand-Archive -Path %TARGET_DIR%\chrome-win64.zip -DestinationPath %TARGET_DIR% -Force"

:: If extracted to a nested folder, move the contents up and remove the extra folder
if exist "%TARGET_DIR%\chrome-win64\chrome.exe" (
    echo Moving extracted files to the correct location...
    move "%TARGET_DIR%\chrome-win64\*" "%TARGET_DIR%\"
    rmdir /S /Q "%TARGET_DIR%\chrome-win64"
)

:: Clean up the zip file after extraction
echo Cleaning up...
del "%TARGET_DIR%\chrome-win64.zip"

:: Confirm completion
echo Chrome has been downloaded and extracted to %TARGET_DIR%.
pause
