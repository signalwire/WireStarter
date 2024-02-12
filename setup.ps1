$PSDefaultParameterValues['Out-File:Encoding'] = 'ASCII'

[System.Environment]::CurrentDirectory
Write-Host $PSScriptRoot

If (Test-Path -Path $PSScriptRoot\.env ) {
# strip the signalwire url from signalwire space (if exists)
((Get-Content -path .env -Raw) -replace '.signalwire.com','') | Set-Content -path .env
docker ps
docker compose -f $PSScriptRoot\docker\docker-compose.yml --env-file $PSScriptRoot\.env --project-name wirestarter up -d
docker exec -it wirestarter /bin/bash
}
Else {

Copy-Item $PSScriptRoot\env.example $PSScriptRoot\.env

$sig_space = read-host "What is your Signalwire space "
$sig_space = $sig_space -replace '.signalwire.com',''   # strip the Signalwire URL if exists
$proj_id = read-host "What is your Signalwire Project ID "
$api_token = read-host "What is your Signalwire REST API token "
$ngrok_token = read-host "What is your NGROK Token (Optional) "
$visual_editor = read-host "What editor to use? nano, vim, emacs "
$work_dir = read-host "Define work directory, C:\SWISH "

Out-File -FilePath $PSScriptRoot\.env -InputObject SIGNALWIRE_SPACE=$sig_space
Out-File -FilePath $PSScriptRoot\.env -Append -InputObject PROJECT_ID=$proj_id
Out-File -FilePath $PSScriptRoot\.env -Append -InputObject REST_API_TOKEN=$api_token
Out-File -FilePath $PSScriptRoot\.env -Append -InputObject NGROK_TOKEN=$ngrok_token
Out-File -FilePath $PSScriptRoot\.env -Append -InputObject VISUAL=$visual_editor
Out-File -FilePath $PSScriptRoot\.env -Append -InputObject WORKDIR=$work_dir

type $PSScriptRoot\.env

docker network create --attachable wirestarter --subnet 172.50.0.0/24
docker compose -f $PSScriptRoot\docker\docker-compose.yml --env-file $PSScriptRoot\.env --project-name wirestarter up -d
docker ps
docker exec -it wirestarter /bin/bash
}
