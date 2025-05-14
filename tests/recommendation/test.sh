#!/usr/bin/env bash
set -euo pipefail

API_HOST="http://127.0.0.1:8000"
USERNAME="admin"
EMAIL=""
PASSWORD="admin123"
PLAYLIST_NAME="test"

echo "==> Logging in..."
loginResp=$(curl -s -X POST -H "Content-Type: application/json" \
  -d "{\"username\":\"${USERNAME}\",\"password\":\"${PASSWORD}\"}" \
  "$API_HOST/api/user/login/")
accessToken=$(echo "$loginResp" | jq -r '.access')
refreshToken=$(echo "$loginResp" | jq -r '.refresh')
echo "Access token: $accessToken"
echo "Refresh token: $refreshToken"

echo -e "\n==> Get Playlist Tracks"
tracksResp=$(curl -s -X GET \
  -H "Authorization: Bearer $accessToken" \
  "$API_HOST/api/playlists/2/tracks/")
echo "Playlist tracks response:"
echo "$tracksResp" | jq .

echo -e "\n==> Get Recommendations"
recsResp=$(curl -s -X GET \
  -H "Authorization: Bearer $accessToken" \
  "$API_HOST/api/playlists/2/recommendations/")
echo "Recommendations response:"
echo "$recsResp" | jq .

echo -e "\n==> Logging out...\n"
logoutResp=$(curl -s -i -X POST \
  -H "Content-Type: application/json" \
  -d "{\"refresh\":\"$refreshToken\"}" \
  "$API_HOST/api/user/logout/")
echo -e "\nLogout response: $logoutResp"

