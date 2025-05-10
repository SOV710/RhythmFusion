#!/usr/bin/env bash
set -euo pipefail

API_URL="http://127.0.0.1:8000/api/music/upload/"
DIR="output"

# 如果没有匹配，则 nullglob 会让 for 循环体跳过
shopt -s nullglob

for file in "${DIR}"/*.json; do
  echo "▶ Uploading ${file}..."
  curl -s -w "\nHTTP status: %{http_code}\n\n" \
       -X POST "${API_URL}" \
       -H "Content-Type: application/json" \
       --data-binary @"${file}"
done
