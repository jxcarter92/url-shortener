#!/bin/bash
set -e

  if ! docker info > /dev/null 2>&1; then
    echo "Docker isn't running. Open Docker Desktop first."
    exit 1
  fi

echo "Starting Container..."
docker start kind-control-plane

until kubectl get nodes > /dev/null 2>&1; do
  sleep 2
  echo "Waiting for the cluster to respond..."
done

echo "Waiting for Nodes..."
kubectl wait --for=condition=Ready nodes --all --timeout=60s

echo "Node status:"
kubectl get nodes

echo "Waiting for Pods..."
kubectl wait --for=condition=Ready pods --all --timeout=90s

echo "Pods Status:"
kubectl get pods
