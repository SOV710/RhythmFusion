#!/usr/bin/env bash
set -euo pipefail

API_HOST="http://127.0.0.1:8000"
USERNAME="test"
EMAIL="test@example.com"
PASSWORD="12345678"
PLAYLIST_NAME="MyTestPlaylist"
SEARCH_KEYWORD="love"
GENRE_CODE="rock"
NEW_PROFILE_NAME="Test User Updated"

# 1. 登录，获取 tokens
echo "1. ==> Logging in..."
loginResp=$(curl -s -X POST -H "Content-Type: application/json" \
  -d "{\"username\":\"${USERNAME}\",\"password\":\"${PASSWORD}\"}" \
  "$API_HOST/api/user/login/")
accessToken=$(echo "$loginResp" | jq -r '.access')
refreshToken=$(echo "$loginResp" | jq -r '.refresh')
echo "Access token: $accessToken"
echo "Refresh token: $refreshToken"

# # 2. 列出所有歌曲
# echo -e "\n2. ==> Fetching all music..."
# curl -i -X GET \
#   -H "Authorization: Bearer $accessToken" \
#   "$API_HOST/api/music/"
#
# # 3. 按关键字搜索
# echo -e "\n3. ==> Searching music with keyword '${SEARCH_KEYWORD}'..."
# curl -i -G \
#   -H "Authorization: Bearer $accessToken" \
#   --data-urlencode "search=${SEARCH_KEYWORD}" \
#   "$API_HOST/api/music/"
#
# # 4. 清除搜索关键字（相当于重新列出所有歌曲）
# echo -e "\n4. ==> Clearing search (fetch all music again)..."
# curl -i -X GET \
#   -H "Authorization: Bearer $accessToken" \
#   "$API_HOST/api/music/"

# 5. 创建新歌单（假设选中歌曲 ID 为 [1,2,3]）
echo -e "\n5. ==> Creating a new playlist '${PLAYLIST_NAME}'..."
createResp=$(curl -s -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $accessToken" \
  -d "{
    \"name\": \"${PLAYLIST_NAME}\",
    \"song_ids\": [1,2,3]
  }" \
  "$API_HOST/api/playlists/")
playlistId=$(echo "$createResp" | jq -r '.id')
echo "Created playlist ID: $playlistId"

# # 6. 查看歌单详情
# echo -e "\n6. ==> Fetching playlist ${playlistId} tracks..."
# curl -i -X GET \
#   -H "Authorization: Bearer $accessToken" \
#   "$API_HOST/api/playlists/${playlistId}/tracks/"
#
# # 7. 向歌单添加新歌曲（假设新增 ID 为 [4,5]）
# echo -e "\n7. ==> Adding songs [4,5] to playlist ${playlistId}..."
# curl -i -X POST \
#   -H "Content-Type: application/json" \
#   -H "Authorization: Bearer $accessToken" \
#   -d '{
#     "song_ids": [4,5]
#   }' \
#   "$API_HOST/api/playlists/${playlistId}/tracks/"
#
# # 8. 从歌单删除歌曲（删除 song_id=2）
# echo -e "\n8. ==> Deleting song 2 from playlist ${playlistId}..."
# curl -i -X DELETE \
#   -H "Authorization: Bearer $accessToken" \
#   "$API_HOST/api/playlists/${playlistId}/tracks/2/"
#
# # 9. 获取歌单推荐
# echo -e "\n9. ==> Fetching recommendations for playlist ${playlistId}..."
# curl -i -X GET \
#   -H "Authorization: Bearer $accessToken" \
#   "$API_HOST/api/playlists/${playlistId}/recommendations/"
#
# # 10. 基于风格推荐
# echo -e "\n10. ==> Fetching genre-based recommendations (genre=${GENRE_CODE})..."
# curl -i -X GET \
#   -H "Authorization: Bearer $accessToken" \
#   "$API_HOST/api/music/genres/${GENRE_CODE}/"
#
# # 11. 获取用户 profile
# echo -e "\n11. ==> Fetching user profile..."
# curl -i -X GET \
#   -H "Accept: application/json" \
#   -H "Authorization: Bearer $accessToken" \
#   "$API_HOST/api/user/profile/"
#
# # 12. 更新用户 profile（修改 name 字段）
# echo -e "\n12. ==> Updating user profile name to '${NEW_PROFILE_NAME}'..."
# curl -i -X PUT \
#   -H "Content-Type: application/json" \
#   -H "Authorization: Bearer $accessToken" \
#   -d "{
#     \"name\": \"${NEW_PROFILE_NAME}\"
#   }" \
#   "$API_HOST/api/user/profile/"
#
# # 13. 登出
# echo -e "\n13. ==> Logging out..."
# curl -i -X POST \
#   -H "Content-Type: application/json" \
#   -H "Authorization: Bearer $accessToken" \
#   -d "{\"refresh\":\"$refreshToken\"}" \
#   "$API_HOST/api/user/logout/"
#
# echo -e "\nAll tests done."
