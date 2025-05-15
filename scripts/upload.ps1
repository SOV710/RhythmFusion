# upload.ps1
$ErrorActionPreference = 'Stop'

$API_URL = 'http://127.0.0.1:8000/api/music/upload/'
$DIR     = 'output'

# 遍历所有 .json 文件
Get-ChildItem -Path $DIR -Filter '*.json' | ForEach-Object {
    $file = $_.FullName
    Write-Host "▶ Uploading $file..."
    # PowerShell 7+ 内置 curl 同名别名，等价于 Invoke-RestMethod
    Invoke-WebRequest `
      -Uri     $API_URL `
      -Method  POST `
      -Headers @{ 'Content-Type' = 'application/json' } `
      -InFile  $file `
      -UseBasicParsing
    Write-Host "`n"
}
