#!/usr/bin/env bash
set -euo pipefail

mkdir -p evidence
docker run -d --name customer-accounts-evidence -p 8080:8080 \
  -e API_TOKEN=capstone-ci-demo customer-accounts:ci
trap 'docker rm -f customer-accounts-evidence >/dev/null 2>&1 || true' EXIT

for attempt in $(seq 1 20); do
  if curl -fsS http://127.0.0.1:8080/health >/dev/null; then break; fi
  sleep 1
done

curl -fsS http://127.0.0.1:8080/ > evidence/kube-app-output.txt
docker images customer-accounts:ci \
  --format 'table {{.Repository}}\t{{.Tag}}\t{{.ID}}\t{{.CreatedSince}}\t{{.Size}}' \
  > evidence/kube-images.txt

capture() {
  local filename="$1"
  shift
  printf '$ ' > "evidence/${filename}.txt"
  printf '%q ' curl "$@" >> "evidence/${filename}.txt"
  printf '\n' >> "evidence/${filename}.txt"
  curl "$@" >> "evidence/${filename}.txt"
  printf '\n' >> "evidence/${filename}.txt"
}

base=(-sS -i -H 'Authorization: Bearer capstone-ci-demo')
capture rest-create-done "${base[@]}" -H 'Content-Type: application/json' \
  -d '{"name":"Ada Lovelace","email":"ada@example.com"}' \
  http://127.0.0.1:8080/accounts
capture rest-list-done "${base[@]}" http://127.0.0.1:8080/accounts
capture rest-read-done "${base[@]}" http://127.0.0.1:8080/accounts/1
capture rest-update-done "${base[@]}" -X PUT -H 'Content-Type: application/json' \
  -d '{"balance":42.5}' http://127.0.0.1:8080/accounts/1
capture rest-delete-done "${base[@]}" -X DELETE http://127.0.0.1:8080/accounts/1

for file in evidence/*.txt; do
  echo "===== ${file} ====="
  cat "$file"
done
