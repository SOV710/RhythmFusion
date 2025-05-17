#!/usr/bin/env bash

API_HOST="http://127.0.0.1:8000"
USERNAME="test"
PASSWORD="12345678"

echo "==> Logging in..."
loginResp=$(curl -s -X POST -H "Content-Type: application/json" \
  -d "{\"username\":\"${USERNAME}\",\"password\":\"${PASSWORD}\"}" \
  "$API_HOST/api/user/login/")
accessToken=$(echo "$loginResp" | jq -r '.access')
refreshToken=$(echo "$loginResp" | jq -r '.refresh')
echo "Access token: $accessToken"
echo "Refresh token: $refreshToken"
