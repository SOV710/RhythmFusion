#!/usr/bin/env bash
set -euo pipefail

API_HOST="http://127.0.0.1:8000"
USERNAME="test"
EMAIL="test@example.com"
PASSWORD="12345678"
WRONG_USER="admin"
WRONG_PASS="admin123"

# 1. 进行一次失败的注册，使用一个已经存在的用户名进行注册，预期回复400
echo -e "1. ==> Registering... (expect for 400)"
firstRegisterResp=$(curl -i -X POST -H "Content-Type: application/json" \
  -d "{
    \"username\": \"${WRONG_USER}\",
    \"password\": \"${WRONG_PASS}\"
  }" \
  "$API_HOST/api/user/register/")
echo -e "first register response: $firstRegisterResp"

# 2. 注册测试，使用未被注册过的用户名进行注册，预期回复201
echo -e "\n\n2. ==> Registering...\n"
secondRegisterResp=$(curl -i -X POST -H "Content-Type: application/json" \
  -d "{
    \"username\": \"${USERNAME}\",
    \"email\": \"${EMAIL}\",
    \"password\": \"${PASSWORD}\"
  }" \
  http://127.0.0.1:8000/api/user/register/)
echo -e "\n\nSecond Register Response is: $secondRegisterResp"

# 3. 测试登录接口，预期回复200
echo "3. ==> Logging in..."
loginResp=$(curl -s -X POST -H "Content-Type: application/json" \
  -d '{"username":"test","password":"12345678"}' \
  "$API_HOST/api/user/login/")
accessToken=$(echo "$loginResp" | jq -r '.access')
refreshToken=$(echo "$loginResp" | jq -r '.refresh')
echo -e "\nTotal response token: $loginResp"
echo -e "\nAccess token: $accessToken"
echo -e "\nRefresh token: $refreshToken"

# 4. 测试认证接口，verify access token，预期回复200
echo -e "\n4. ==> Verifying access token..."
firstVerifyAccess=$(curl -i -X POST \
  -H "Content-Type: application/json" \
  -d "{\"token\":\"$accessToken\"}" \
  "$API_HOST/api/user/verify/")
echo -e "\nTotal response token: $firstVerifyAccess"

# 5. 经过认证access token仍然能使用后，测试profile接口
echo -e "\n5. ==> Fetching profile (should 200)...\n"
curl -i -X GET \
  -H "Accept: application/json" \
  -H "Authorization: Bearer $accessToken" \
  "$API_HOST/api/user/profile/"

# 现在等待六分钟，等待access token过期
echo -e "\n\n==> Waiting 6 minutes…"
sleep 360

# 6. 再测试认证接口，verify access token，预期回复401
echo -e "\n6. ==> Verifying access token..."
secondVerifyAccess=$(curl -i -X POST \
  -H "Content-Type: application/json" \
  -d "{\"token\":\"$accessToken\"}" \
  "$API_HOST/api/user/verify/")
echo -e "\nTotal response token: $secondVerifyAccess"

# 7. 发现401错误，正常应该用 refresh token 刷新 access
echo -e "\n\n7. ==> Refreshing access token…\n"
newLoginResp=$(curl -s -X POST \
  -H "Content-Type: application/json" \
  -d "{\"refresh\":\"$refreshToken\"}" \
  "$API_HOST/api/user/refresh/")
newAccess=$(echo "$newLoginResp" | jq -r '.access')
echo -e "\nNew refresh response token: $newLoginResp"
echo -e "\nNew access token: $newAccess"

# 8. 再尝试fetch profile （预期输出200）
echo -e "\n8. ==> Fetching profile (should 200)...\n"
curl -i -X GET \
  -H "Accept: application/json" \
  -H "Authorization: Bearer $newAccess" \
  "$API_HOST/api/user/profile/"

# 9. 老调重弹，logout之前也要verify一下access token
echo -e "\n9. ==> Verifying access token..."
thirdVerifyAccess=$(curl -i -X POST \
  -H "Content-Type: application/json" \
  -d "{\"token\":\"$newAccess\"}" \
  "$API_HOST/api/user/verify/")
echo -e "\nTotal response token: $thirdVerifyAccess"

# 10. Logout
echo -e "\n\n10. ==> Logging out...\n"
logoutResp=$(curl -i -X POST \
  -H "Authorization: Bearer $newAccess" \
  -H "Content-Type: application/json" \
  -d "{\"refresh\":\"$refreshToken\"}" \
  "$API_HOST/api/user/logout/")
echo -e "\nLogout response: $logoutResp"

sleep 10

# 11. 再尝试用 refresh token 刷新 access（应该失效，401）
echo -e "\n\n11. ==> Refreshing access token…\n"
newnewLoginResp=$(curl -s -X POST \
  -H "Content-Type: application/json" \
  -d "{\"refresh\":\"$refreshToken\"}" \
  "$API_HOST/api/user/refresh/")
echo "Response token: $newnewLoginResp"
