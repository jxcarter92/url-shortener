#!/bin/bash
set -e

echo "Building out for testnet..."
docker build -t url-shortener:test .

echo "Running testnet..."
docker run --rm -p 5000:5000 --network testnet -e REDIS_HOST=redis-test url-shortener:test
