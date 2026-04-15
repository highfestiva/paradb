#!/bin/bash
set -e

# 1. Start minikube with the Docker driver
minikube start --driver=docker

# 2. Point your shell to minikube's Docker daemon
eval $(minikube docker-env)          # Linux/macOS
# minikube docker-env | Invoke-Expression   # PowerShell

# 3. Build the container images inside minikube's Docker
docker build -t paradb-orchestrator:latest -f Dockerfile.orchestrator .
docker build -t paradb-shard:latest        -f Dockerfile.shard .

# 4. Apply the Kubernetes manifests
kubectl apply -f k8s/

# 5. Wait for pods to become ready
echo "Waiting for pods..."
kubectl -n paradb rollout status deployment/orchestrator --timeout=60s
kubectl -n paradb rollout status deployment/shard --timeout=60s

# 6. Expose the shard service to localhost
echo "Shard URL:"
minikube service shard -n paradb --url
# Use the printed URL as the base for API calls
