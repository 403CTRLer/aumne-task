#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
SPEC_PATH="$ROOT_DIR/sdk/openapi.json"
OUTPUT_DIR="$ROOT_DIR/sdk/python-client"
IMAGE="openapitools/openapi-generator-cli:v7.5.0"

echo "[sdk] Downloading OpenAPI specification"
curl -fsSL "http://localhost:8000/openapi.json" -o "$SPEC_PATH"

if [ -d "$OUTPUT_DIR" ]; then
  echo "[sdk] Removing existing client"
  rm -rf "$OUTPUT_DIR"
fi

echo "[sdk] Generating client via Docker"
docker run --rm -v "$ROOT_DIR:/local" \
  "$IMAGE" generate \
  -i /local/sdk/openapi.json \
  -g python \
  -o /local/sdk/python-client \
  --additional-properties=packageName=python_client,projectName=whatsapp_appointment_sdk

echo "[sdk] Client available in sdk/python-client"

