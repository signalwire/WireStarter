@echo off
REM Create the C:/SWISH directory if it does not already exist
mkdir "C:/SWISH"

REM Pull the briankwest/wirestarter Docker image
docker pull briankwest/wirestarter

REM Check if the container "wirestarter" already exists
docker ps -a --format "{{.Names}}" | findstr /B "wirestarter" > nul
if %ERRORLEVEL% equ 0 (
    echo Container "wirestarter" already exists.
    set /p USE_EXISTING="Do you want to use the existing container (y/n)? "
    if /I "%USE_EXISTING%"=="y" (
        echo Checking if "wirestarter" container is running...
        docker ps --format "{{.Names}}" | findstr /B "wirestarter" > nul
        if %ERRORLEVEL% neq 0 (
            echo Starting the "wirestarter" container...
            docker start wirestarter
        ) else (
            echo Container "wirestarter" is already running.
        )
        goto ExecShell
    ) else if /I "%USE_EXISTING%"=="n" (
        echo Removing the existing "wirestarter" container...
        docker rm -f wirestarter
        goto CreateNew
    ) else (
        echo Invalid option. Exiting...
        exit /b
    )
) else (
    echo No existing container named "wirestarter". Creating new one...
    goto CreateNew
)

:CreateNew
REM Run a new container named "wirestarter" from the pulled image
docker run -it -d --name wirestarter --env-file .env --volume "C:/SWISH:/workdir" --volume opt:/opt briankwest/wirestarter /start_services.sh || echo "up"
goto ExecShell

:ExecShell
REM Executing a bash shell inside the "wirestarter" container
docker start wirestarter
docker exec -it wirestarter bash

echo Container "wirestarter" is running and a bash shell has been executed inside it.
pause
