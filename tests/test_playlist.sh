#!/usr/bin/env bash
# tests/playlist_flow.sh
set -euo pipefail

API="http://127.0.0.1:8000"
USER="test"
PASS="12345678"

# 1. 登录，拿到 access token
echo "==> 1. login"
login_resp=$(curl -s -o login.json -w "%{http_code}" -X POST \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"${USER}\",\"password\":\"${PASS}\"}" \
  "$API/api/user/login/")
if [[ "$login_resp" != "200" ]]; then
  echo "Login failed, status=$login_resp"; cat login.json; exit 1
fi
access=$(jq -r .access login.json)
echo "  -> access={$access}"

# 2. 创建歌单
echo -e "\n==> 2. create playlist"
create_code=$(curl -s -o create.json -w "%{http_code}" -X POST \
  -H "Accept: application/json" \
  -H "Authorization: Bearer ${access}" \
  -H "Content-Type: application/json" \
  -d '{"name":"My Playlist"}' \
  "$API/api/playlists/")
if [[ "$create_code" != "201" ]]; then
  echo "  ❌ expected 201, got $create_code"; cat create.json; exit 1
fi
echo "  ✔ status=201"
jq . create.json
playlist_id=$(jq -r .id create.json)

# 预期响应体（示例）：
# {
#   "id": 1,
#   "name": "My Playlist",
#   "created_at": "2025-05-11T12:34:56.123456Z",
#   "updated_at": "2025-05-11T12:34:56.123456Z"
# }

# 3. 获取歌单详情
echo -e "\n==> 3. get playlist detail"
detail_code=$(curl -s -o detail.json -w "%{http_code}" \
  -H "Accept: application/json" \
  -H "Authorization: Bearer ${access}" \
  "$API/api/playlists/${playlist_id}/")
if [[ "$detail_code" != "200" ]]; then
  echo "  ❌ expected 200, got $detail_code"; cat detail.json; exit 1
fi
echo "  ✔ status=200"
jq . detail.json

# 预期响应体 = 步骤 2 中的 JSON

# 4. 列出曲目（初次，应为空）
echo -e "\n==> 4. list tracks (empty)"
list_code=$(curl -s -o list1.json -w "%{http_code}" \
  -H "Accept: application/json" \
  -H "Authorization: Bearer ${access}" \
  "$API/api/playlists/${playlist_id}/tracks/")
if [[ "$list_code" != "200" ]]; then
  echo "  ❌ expected 200, got $list_code"; exit 1
fi
echo "  ✔ status=200"
jq . list1.json

# 预期响应体：
# []

# 5. 添加曲目 ID=1
echo -e "\n==> 5. add song 1"
add_code=$(curl -s -o add.json -w "%{http_code}" -X POST \
  -H "Accept: application/json" \
  -H "Authorization: Bearer ${access}" \
  -H "Content-Type: application/json" \
  -d '{"song_id":1}' \
  "$API/api/playlists/${playlist_id}/tracks/")
if [[ "$add_code" != "201" ]]; then
  echo "  ❌ expected 201, got $add_code"; cat add.json; exit 1
fi
echo "  ✔ status=201"
jq . add.json

# 预期响应体：
# {"detail":"song added"}

# 6. 再次列出曲目（应包含刚才添加的那首）
echo -e "\n==> 6. list tracks (1 song)"
curl -s -H "Accept: application/json" -H "Authorization: Bearer ${access}" \
  "$API/api/playlists/${playlist_id}/tracks/" | jq .

# 预期响应体示例：
# [
#   {
#     "id": 1,
#     "title": "歌曲标题",
#     "artist": "演唱者",
#     ...其它 SongSerializer 字段
#   }
# ]

# 7. 删除曲目 ID=1
echo -e "\n==> 7. delete song 1"
del_code=$(curl -s -o /dev/null -w "%{http_code}" -X DELETE \
  -H "Authorization: Bearer ${access}" \
  "$API/api/playlists/${playlist_id}/tracks/1/")
if [[ "$del_code" != "204" ]]; then
  echo "  ❌ expected 204, got $del_code"; exit 1
fi
echo "  ✔ status=204 (no content)"

# 8. 再次列出曲目（应恢复为空）
echo -e "\n==> 8. list tracks (empty again)"
curl -s -H "Accept: application/json" -H "Authorization: Bearer ${access}" \
  "$API/api/playlists/${playlist_id}/tracks/" | jq .

# 预期响应体：
# []

# 9. 推荐（尚未实现）
echo -e "\n==> 9. recommendations"
rec_code=$(curl -s -o rec.json -w "%{http_code}" \
  -H "Accept: application/json" \
  -H "Authorization: Bearer ${access}" \
  "$API/api/playlists/${playlist_id}/recommendations/")
if [[ "$rec_code" != "501" ]]; then
  echo "  ❌ expected 501, got $rec_code"; cat rec.json; exit 1
fi
echo "  ✔ status=501"
jq . rec.json

# 预期响应体：
# {"detail":"Not implemented yet."}

echo -e "\n✅ All playlist tests passed."
