# test_auth.ps1
$ErrorActionPreference = 'Stop'

$API_HOST = 'http://127.0.0.1:8000'
$USERNAME = 'test'
$EMAIL = 'test@example.com'
$PASSWORD = '12345678'
$WRONG_USER = 'admin'
$WRONG_PASS = 'admin123'

# 1. 失败注册
Write-Host "1. ==> Registering... (expect 400)"
try {
    $firstRegisterResp = Invoke-RestMethod -Method Post -Uri "$API_HOST/api/user/register/" `
        -Headers @{ 'Content-Type' = 'application/json' } `
        -Body (@{ username = $WRONG_USER; password = $WRONG_PASS } | ConvertTo-Json)
    Write-Host "Unexpected success: $firstRegisterResp"
} catch {
    Write-Host "Expected error response: $($_.Exception.Response.StatusCode.value__)"
    $stream = $_.Exception.Response.GetResponseStream()
    $reader = New-Object IO.StreamReader($stream)
    $errorContent = $reader.ReadToEnd()
    Write-Host "Error content: $errorContent"
}

# 2. 正常注册
Write-Host "`n2. ==> Registering new user..."
$secondRegisterResp = Invoke-RestMethod -Method Post -Uri "$API_HOST/api/user/register/" `
    -Headers @{ 'Content-Type' = 'application/json' } `
    -Body (@{ username = $USERNAME; email = $EMAIL; password = $PASSWORD } | ConvertTo-Json)
Write-Host "Second Register Response: $secondRegisterResp"

# 3. 登录
Write-Host "3. ==> Logging in..."
$loginResp = Invoke-RestMethod -Method Post -Uri "$API_HOST/api/user/login/" `
    -Headers @{ 'Content-Type' = 'application/json' } `
    -Body (@{ username = $USERNAME; password = $PASSWORD } | ConvertTo-Json)
$accessToken = $loginResp.access
$refreshToken = $loginResp.refresh
Write-Host "Access token: $accessToken"
Write-Host "Refresh token: $refreshToken"

# 4. 验证 access_token
Write-Host "`n4. ==> Verifying access token..."
$verifyResp1 = Invoke-RestMethod -Method Post -Uri "$API_HOST/api/user/verify/" `
    -Headers @{ 'Content-Type' = 'application/json' } `
    -Body (@{ token = $accessToken } | ConvertTo-Json)
Write-Host "Verify response: $verifyResp1"

# 5. 获取 profile
Write-Host "`n5. ==> Fetching profile (should 200)..."
Invoke-RestMethod -Method Get -Uri "$API_HOST/api/user/profile/" `
    -Headers @{
        'Accept' = 'application/json'
        'Authorization' = "Bearer $accessToken"
    } | Write-Host

# 等待 6 分钟
Write-Host "`n==> Waiting 6 minutes..."
Start-Sleep -Seconds 360

# 6. 再次验证 access_token (expect 401)
Write-Host "`n6. ==> Verifying access token..."
try {
    $verifyResp2 = Invoke-RestMethod -Method Post -Uri "$API_HOST/api/user/verify/" `
        -Headers @{ 'Content-Type' = 'application/json' } `
        -Body (@{ token = $accessToken } | ConvertTo-Json)
    Write-Host "Unexpected success: $verifyResp2"
} catch {
    Write-Host "Expected error on verify: $($_.Exception.Response.StatusCode.value__)"
}

# 7. 刷新 access_token
Write-Host "`n7. ==> Refreshing access token..."
$newLoginResp = Invoke-RestMethod -Method Post -Uri "$API_HOST/api/user/refresh/" `
    -Headers @{ 'Content-Type' = 'application/json' } `
    -Body (@{ refresh = $refreshToken } | ConvertTo-Json)
$newAccess = $newLoginResp.access
Write-Host "New access token: $newAccess"

# 8. 再次获取 profile
Write-Host "`n8. ==> Fetching profile (should 200)..."
Invoke-RestMethod -Method Get -Uri "$API_HOST/api/user/profile/" `
    -Headers @{
        'Accept' = 'application/json'
        'Authorization' = "Bearer $newAccess"
    } | Write-Host

# 9. 验证新 access_token
Write-Host "`n9. ==> Verifying new access token..."
$verifyResp3 = Invoke-RestMethod -Method Post -Uri "$API_HOST/api/user/verify/" `
    -Headers @{ 'Content-Type' = 'application/json' } `
    -Body (@{ token = $newAccess } | ConvertTo-Json)
Write-Host "Verify response: $verifyResp3"

# 10. 登出
Write-Host "`n10. ==> Logging out..."
$logoutResp = Invoke-RestMethod -Method Post -Uri "$API_HOST/api/user/logout/" `
    -Headers @{ 'Authorization' = "Bearer $newAccess"; 'Content-Type' = 'application/json' } `
    -Body (@{ refresh = $refreshToken } | ConvertTo-Json)
Write-Host "Logout response: $logoutResp"

Start-Sleep -Seconds 10

# 11. 再次刷新 (should 401)
Write-Host "`n11. ==> Refreshing access token..."
try {
    $newnewLoginResp = Invoke-RestMethod -Method Post -Uri "$API_HOST/api/user/refresh/" `
        -Headers @{ 'Content-Type' = 'application/json' } `
        -Body (@{ refresh = $refreshToken } | ConvertTo-Json)
    Write-Host "Unexpected success: $newnewLoginResp"
} catch {
    Write-Host "Expected error on refresh after logout: $($_.Exception.Response.StatusCode.value__)"
}
