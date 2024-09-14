@echo off
setlocal EnableDelayedExpansion

REM Check if the batch file is running in a Command Prompt window and relaunch it if not
if not "%~1"=="relaunched" (
    start cmd /k ""%~f0" relaunched"
    exit /b
)

REM Create the C:/SWISH directory if it does not already exist
mkdir "C:/SWISH"

REM Check if C:/SWISH/.env file exists, if not, copy env.example to C:/SWISH/.env
if not exist "C:/SWISH/.env" (
    copy "env.example" "C:/SWISH/.env"
    echo The .env file has been copied to C:/SWISH/.env from env.example.
)

echo Please edit the .env file to set the required options.
notepad "C:/SWISH/.env"

echo Checking if Docker Desktop is running...

tasklist /FI "IMAGENAME eq Docker Desktop.exe" 2>NUL | find /I /N "Docker Desktop.exe" >NUL
if "%ERRORLEVEL%"=="0" (
    echo Docker Desktop is already running.
) else (
    echo Starting Docker Desktop...
    start "" "C:\Program Files\Docker\Docker\Docker Desktop.exe"
    
    echo Waiting for Docker Desktop to start...
    timeout /t 10 /nobreak >NUL 2>&1

    :CHECK_DOCKER
    tasklist /FI "IMAGENAME eq Docker Desktop.exe" 2>NUL | find /I /N "Docker Desktop.exe" >NUL
    if "%ERRORLEVEL%"=="0" (
        echo Docker Desktop has started successfully.
    ) else (
        echo Docker Desktop is still not running. Retrying...
        timeout /t 5 /nobreak >NUL 2>&1
        goto CHECK_DOCKER
    )
)

echo Continuing with the rest of the batch script...

REM Pull the briankwest/wirestarter Docker image
docker pull briankwest/wirestarter

REM Check if the container "wirestarter" already exists
docker ps -a --format "{{.Names}}" | findstr /B "wirestarter" > nul
if %ERRORLEVEL% equ 0 (
    echo Container "wirestarter" already exists.
    set /p USE_EXISTING="Do you want to use the existing container (y/n)? "
    echo You selected: '!USE_EXISTING!'

    if /I "!USE_EXISTING!"=="y" (
        echo Checking if "wirestarter" container is running...
        docker ps --format "{{.Names}}" | findstr /B "wirestarter" > nul
        if %ERRORLEVEL% neq 0 (
            echo Starting the "wirestarter" container...
            docker start wirestarter
        ) else (
            echo Container "wirestarter" is already running.
        )
        goto ExecShell
    ) else if /I "!USE_EXISTING!"=="n" (
        echo Removing the existing "wirestarter" container...
        docker rm -f wirestarter
        goto CreateNew
    ) else (
        echo Invalid option. Exiting...
        pause
        exit /b
    )
) else (
    echo No existing container named "wirestarter". Creating new one...
    goto CreateNew
)

:CreateNew
REM Run a new container named "wirestarter" from the pulled image
docker run -it -d --name wirestarter --env-file "C:/SWISH/.env" --volume "C:/SWISH:/workdir" --volume opt:/opt briankwest/wirestarter /start_services.sh || echo "up"
goto ExecShell

:ExecShell
REM Executing a bash shell inside the "wirestarter" container
docker start wirestarter
docker exec -it wirestarter bash

echo Container "wirestarter" is running and a bash shell has been executed inside it.
pause
