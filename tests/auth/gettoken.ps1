# login_and_setup.ps1
$ErrorActionPreference = 'Stop'

$API_HOST        = 'http://127.0.0.1:8000'
$USERNAME        = 'test'
$PASSWORD        = '12345678'

Write-Host "==> Logging in..."
$loginResp = Invoke-RestMethod -Method Post -Uri "$API_HOST/api/user/login/" `
    -Headers @{ 'Content-Type' = 'application/json' } `
    -Body (@{ username = $USERNAME; password = $PASSWORD } | ConvertTo-Json)

$accessToken  = $loginResp.access
$refreshToken = $loginResp.refresh

Write-Host "Access token: $accessToken"
Write-Host "Refresh token: $refreshToken"