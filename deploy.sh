#!/bin/bash

set -e

if [ -z "$1" ]; then
  echo "Usage: ./deploy.sh <version>   (example: ./deploy.sh v6)"
  exit 1
fi

echo "building... "
docker build -t url-shortener:$1 .
 
echo "loading..."
kind load docker-image url-shortener:$1

echo "updating image tag in deployment.yaml"
sed -i "s|image: url-shortener:.*|image: url-shortener:$1|" deployment.yaml

echo "applying to files..."
kubectl apply -f .

echo "rollout on build."
kubectl rollout status deployment/url-shortener


