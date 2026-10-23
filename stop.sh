#!/bin/bash
set -e

echo "Stopping containers.."
docker stop kind-control-plane

echo "Running containers (should be empty):"
docker ps
echo "cluster stopped."
