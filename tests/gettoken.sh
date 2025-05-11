#!/usr/bin/env bash

API_HOST="http://127.0.0.1:8000"
USERNAME="test"
EMAIL="test@example.com"
PASSWORD="12345678"
PLAYLIST_NAME="MyTestPlaylist"
SEARCH_KEYWORD="love"
GENRE_CODE="rock"
NEW_PROFILE_NAME="Test User Updated"

echo "1. ==> Logging in..."
loginResp=$(curl -s -X POST -H "Content-Type: application/json" \
  -d "{\"username\":\"${USERNAME}\",\"password\":\"${PASSWORD}\"}" \
  "$API_HOST/api/user/login/")
accessToken=$(echo "$loginResp" | jq -r '.access')
refreshToken=$(echo "$loginResp" | jq -r '.refresh')
echo "Access token: $accessToken"
echo "Refresh token: $refreshToken"
