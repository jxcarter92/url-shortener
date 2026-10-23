#!/bin/bash
set -e

echo "Running port-forward"
kubectl port-forward service/url-shortener 8080:80      
