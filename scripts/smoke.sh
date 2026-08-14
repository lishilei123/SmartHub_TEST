#!/usr/bin/env sh
set -eu
BASE="${BASE_URL:-http://localhost:8000}"
echo "[1/3] health"
curl -fsS "$BASE/api/health"
echo
echo "[2/3] login"
TOKEN=$(curl -fsS -X POST "$BASE/api/login" -H 'Content-Type: application/json' -d '{"username":"admin","password":"admin123"}' | sed -n 's/.*"token":"\([^"]*\)".*/\1/p')
test -n "$TOKEN"
echo "[3/3] projects"
curl -fsS "$BASE/api/projects" -H "Authorization: Bearer $TOKEN" >/dev/null
echo "smoke passed"
