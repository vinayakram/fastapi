#!/usr/bin/env bash
set -o errexit

echo "=== Installing Python dependencies ==="
pip install -r requirements.txt

echo "=== Building React Frontend ==="
cd frontend
npm install
npm run build
cd ..

echo "=== Build Complete ==="
