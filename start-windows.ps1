# Define functions
function CreateNew {
    docker run -it -d --name wirestarter --env-file "C:/SWISH/.env" --volume "C:/SWISH:/workdir" --volume opt:/opt briankwest/wirestarter /start_services.sh
    ExecShell
}

function ExecShell {
    docker start wirestarter
    docker exec -it wirestarter bash
    Write-Host "Container 'wirestarter' is running and a bash shell has been executed inside it."
}

# Create the C:/SWISH directory if it does not already exist
if (-Not (Test-Path "C:/SWISH")) {
    New-Item -Path "C:/SWISH" -ItemType Directory
}

# Check if C:/SWISH/.env file exists, if not, copy env.example to C:/SWISH/.env
if (-Not (Test-Path "C:/SWISH/.env")) {
    Copy-Item -Path "env.example" -Destination "C:/SWISH/.env"
    Write-Host "The .env file has been copied to C:/SWISH/.env from env.example."
}

# Prompt the user to edit the .env file
Write-Host "Please edit the .env file to set the required options."
& notepad.exe "C:/SWISH/.env"
Write-Host "Waiting for you to finish editing the .env file..."

# Pull the briankwest/wirestarter Docker image
docker pull briankwest/wirestarter

# Check if the container "wirestarter" already exists
$containerExists = docker ps -a --format "{{.Names}}" | Select-String -Pattern "^wirestarter$"

if ($containerExists) {
    Write-Host "Container 'wirestarter' already exists."
    $useExisting = Read-Host "Do you want to use the existing container (y/n)?"
    switch ($useExisting.ToLower()) {
        "y" {
            Write-Host "Checking if 'wirestarter' container is running..."
            $containerRunning = docker ps --format "{{.Names}}" | Select-String -Pattern "^wirestarter$"
            if (-Not $containerRunning) {
                Write-Host "Starting the 'wirestarter' container..."
                docker start wirestarter
            } else {
                Write-Host "Container 'wirestarter' is already running."
            }
            ExecShell
        }
        "n" {
            Write-Host "Removing the existing 'wirestarter' container..."
            docker rm -f wirestarter
            CreateNew
        }
        default {
            Write-Host "Invalid option. Exiting..."
            exit
        }
    }
} else {
    Write-Host "No existing container named 'wirestarter'. Creating new one..."
    CreateNew
}

# Pauses the script execution and waits for user input before closing
Read-Host "Press Enter to exit..."
