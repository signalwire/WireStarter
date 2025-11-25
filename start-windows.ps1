# Start of the PowerShell script

# Function to ensure the execution policy is set to RemoteSigned
function Ensure-ExecutionPolicy {
    $currentPolicy = Get-ExecutionPolicy -Scope CurrentUser
    if ($currentPolicy -ne 'RemoteSigned') {
        Write-Host "Current execution policy is '$currentPolicy'. Attempting to set it to 'RemoteSigned'."
        try {
            Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force -ErrorAction Stop
            Write-Host "Execution policy set to 'RemoteSigned' for CurrentUser."
        } catch {
            Write-Warning "Failed to set execution policy. Administrative privileges may be required."
            # Check if running as Administrator
            $IsAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
            if (-not $IsAdmin) {
                Write-Host "This script needs to be run as Administrator to change the execution policy."
                $scriptPath = $MyInvocation.MyCommand.Definition
                Write-Host "Relaunching the script with administrative privileges..."
                Write-Host "If the script ends, please start it again..."
                Start-Process powershell "-ExecutionPolicy Bypass -File `"$scriptPath`"" -Verb RunAs
                Pause
                exit
            } else {
                Write-Error "Even with administrative privileges, failed to set execution policy. Exiting."
                Pause
                exit
            }
        }
    } else {
        Write-Host "Execution policy is already set to 'RemoteSigned' for CurrentUser."
    }
}

# Function to check and start Docker Desktop if necessary
function Start-DockerDesktop {
    Write-Host "Checking if Docker Desktop is running..."
    $dockerProcess = Get-Process -Name 'Docker Desktop' -ErrorAction SilentlyContinue
    if (-not $dockerProcess) {
        Write-Host "Docker Desktop is not running. Starting Docker Desktop..."
        $dockerDesktopPath = "C:\Program Files\Docker\Docker\Docker Desktop.exe"
        if (-not (Test-Path $dockerDesktopPath)) {
            Write-Error "Docker Desktop executable not found at $dockerDesktopPath"
            Pause
            exit
        }
        Start-Process -FilePath $dockerDesktopPath
        Write-Host "Waiting for Docker Desktop to start..."
        Start-Sleep -Seconds 10

        while (-not (Get-Process -Name 'Docker Desktop' -ErrorAction SilentlyContinue)) {
            Write-Host "Docker Desktop is still not running. Retrying in 5 seconds..."
            Start-Sleep -Seconds 5
        }
        Write-Host "Docker Desktop process has started."
    } else {
        Write-Host "Docker Desktop is already running."
    }

    # Wait until the Docker daemon is responsive
    Write-Host "Waiting for Docker daemon to become responsive..."
    $maxAttempts = 30
    $attempt = 0
    while ($attempt -lt $maxAttempts) {
        try {
            docker info | Out-Null
            Write-Host "Docker daemon is responsive."
            break
        } catch {
            Write-Host "Docker daemon not yet responsive. Retrying in 5 seconds..."
            Start-Sleep -Seconds 5
            $attempt++
        }
    }

    if ($attempt -eq $maxAttempts) {
        Write-Error "Docker daemon did not become responsive in a timely manner. Exiting."
        Pause
        exit
    }
}

# Function to create a new container
function CreateNewContainer {
    Write-Host "Creating a new 'wirestarter' container..."
    docker run -it -d --name wirestarter --env-file "${envFileDestination}" --volume "${swishPath}:/workdir" --volume opt:/opt briankwest/wirestarter /start_services.sh
    StartAndExecShell
}

# Function to start the container and execute a bash shell inside it
function StartAndExecShell {
    Write-Host "Starting the 'wirestarter' container..."
    docker start wirestarter | Out-Null
    Write-Host "Executing a bash shell inside the 'wirestarter' container..."
    docker exec -it wirestarter bash
    Write-Host "Exited the bash shell inside the 'wirestarter' container."
}

# Main script execution starts here

# Ensure Execution Policy is set to RemoteSigned
Ensure-ExecutionPolicy

# Create the C:/SWISH directory if it does not already exist
$swishPath = "C:/SWISH"
if (-not (Test-Path $swishPath)) {
    New-Item -Path $swishPath -ItemType Directory | Out-Null
}

# Check if C:/SWISH/.env file exists, if not, copy env.example to C:/SWISH/.env
$envFileSource = "env.example"
$envFileDestination = "${swishPath}/.env"
if (-not (Test-Path $envFileDestination)) {
    if (-not (Test-Path $envFileSource)) {
        Write-Error "The env.example file was not found in the current directory."
        Pause
        exit
    }
    Copy-Item -Path $envFileSource -Destination $envFileDestination
    Write-Host "The .env file has been copied to $envFileDestination from $envFileSource."
}

# Check if the .env file needs to be edited
$requiredVariables = @("SIGNALWIRE_SPACE_NAME", "SIGNALWIRE_PROJECT_ID", "SIGNALWIRE_TOKEN", "NGROK_TOKEN", "VISUAL", "WORKDIR")
$envVariables = @{}

Get-Content $envFileDestination | ForEach-Object {
    $line = $_.Trim()
    if ($line -and -not $line.StartsWith("#")) {
        $parts = $line -split '=', 2
        if ($parts.Length -eq 2) {
            $key = $parts[0].Trim()
            $value = $parts[1].Trim()
            $envVariables[$key] = $value
        }
    }
}

$variablesNotSet = @()
foreach ($var in $requiredVariables) {
    if (-not ($envVariables.ContainsKey($var) -and $envVariables[$var])) {
        $variablesNotSet += $var
    }
}

if ($variablesNotSet.Count -gt 0) {
    Write-Host "The following required variables are not set in the .env file:"
    $variablesNotSet | ForEach-Object { Write-Host "- $_" }
    Write-Host "Please edit the .env file to set the required options."
    Start-Process -FilePath "notepad.exe" -ArgumentList $envFileDestination -Wait
} else {
    Write-Host "All required environment variables are set in the .env file."
}

# Start Docker Desktop if not running
Start-DockerDesktop

Write-Host "Continuing with the rest of the script..."

# Pull the briankwest/wirestarter Docker image
Write-Host "Pulling the 'briankwest/wirestarter' Docker image..."
docker pull briankwest/wirestarter

# Check if the container "wirestarter" already exists
$containerExists = docker ps -a --format "{{.Names}}" | Select-String -Pattern "^wirestarter$" -Quiet

if ($containerExists) {
    Write-Host "Container 'wirestarter' already exists."
    $useExisting = Read-Host "Do you want to use the existing container (y/n)? "
    Write-Host "You selected: '$useExisting'"

    if ($useExisting -match '^[Yy]$') {
        # Check if the container is running
        $containerRunning = docker ps --format "{{.Names}}" | Select-String -Pattern "^wirestarter$" -Quiet
        if (-not $containerRunning) {
            Write-Host "Starting the 'wirestarter' container..."
            docker start wirestarter
        } else {
            Write-Host "Container 'wirestarter' is already running."
        }
        # Execute bash shell inside the container
        StartAndExecShell
    } elseif ($useExisting -match '^[Nn]$') {
        Write-Host "Removing the existing 'wirestarter' container..."
        docker rm -f wirestarter
        CreateNewContainer
    } else {
        Write-Host "Invalid option. Exiting..."
        Pause
        exit
    }
} else {
    Write-Host "No existing container named 'wirestarter'. Creating new one..."
    CreateNewContainer
}

Pause  # Wait for user input before closing
