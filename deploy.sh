#!/bin/bash

set -e

SHA=$(git rev-parse HEAD) 
echo $SHA

echo "updating image tag in deployment.yaml"
sed -i "s|ghcr.io/jxcarter92/url-shortener:.*|ghcr.io/jxcarter92/url-shortener:$SHA|" deployment.yaml

echo "applying to files..."
kubectl apply -f deployment.yaml

echo "rollout on build."
kubectl rollout status deployment/url-shortener


