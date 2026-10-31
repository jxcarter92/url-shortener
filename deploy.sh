#!/bin/bash

set -eu
SHORT_SHA=$(git rev-parse --short HEAD)
SHA=$(git rev-parse HEAD) 
echo $SHA

echo "updating image tag in deployment.yaml"
sed -i "s|ghcr.io/jxcarter92/url-shortener:.*|ghcr.io/jxcarter92/url-shortener:$SHA|" deployment.yaml

echo "applying to files..."
kubectl apply -f deployment.yaml

echo "rollout on build."
kubectl rollout status deployment/url-shortener

echo "adding deployment.yanl"
git add deployment.yaml

echo "committing..."
git commit -m "Deploy $SHORT_SHA [skip ci]"

echo "push..."
git push
