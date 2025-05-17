# test_recommend.ps1
$ErrorActionPreference = 'Stop'

$API_HOST = 'http://127.0.0.1:8000'
$USERNAME = 'admin'
$PASSWORD = 'admin123'

Write-Host "==> Logging in..."
$loginResp = Invoke-RestMethod -Method Post -Uri "$API_HOST/api/user/login/" `
    -Headers @{ 'Content-Type' = 'application/json' } `
    -Body (@{ username = $USERNAME; password = $PASSWORD } | ConvertTo-Json)
$accessToken = $loginResp.access
$refreshToken = $loginResp.refresh
Write-Host "Access token: $accessToken"
Write-Host "Refresh token: $refreshToken"

Write-Host "`n==> Get Playlist Tracks"
$tracksResp = Invoke-RestMethod -Method Get -Uri "$API_HOST/api/playlists/2/tracks/" `
    -Headers @{ 'Authorization' = "Bearer $accessToken" }
Write-Host "Playlist tracks response:"
$tracksResp | ConvertTo-Json | Write-Host

Write-Host "`n==> Get Recommendations"
$recsResp = Invoke-RestMethod -Method Get -Uri "$API_HOST/api/playlists/2/recommendations/" `
    -Headers @{ 'Authorization' = "Bearer $accessToken" }
Write-Host "Recommendations response:"
$recsResp | ConvertTo-Json | Write-Host

Write-Host "`n==> Logging out..."
$logoutResp = Invoke-RestMethod -Method Post -Uri "$API_HOST/api/user/logout/" `
    -Headers @{ 'Content-Type' = 'application/json' } `
    -Body (@{ refresh = $refreshToken } | ConvertTo-Json)
Write-Host "Logout response: $logoutResp"
