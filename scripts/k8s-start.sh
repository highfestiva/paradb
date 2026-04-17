#!/bin/bash
set -e

# Requires: Docker Desktop with Kubernetes enabled
# (Settings -> Kubernetes -> Enable Kubernetes)

# 1. Verify Docker Desktop K8s is the active context
kubectl config use-context docker-desktop

# 2. Build the container images (Docker Desktop shares its daemon with K8s)
docker build -t paradb-orchestrator:latest -f Dockerfile.orchestrator .
docker build -t paradb-shard:latest        -f Dockerfile.shard .

# 3. Apply the Kubernetes manifests
kubectl apply -f k8s/

# 4. Wait for pods to become ready
echo "Waiting for pods..."
kubectl -n paradb rollout status deployment/orchestrator --timeout=60s
kubectl -n paradb rollout status deployment/shard --timeout=60s

echo "Shard API available at http://localhost:3357"
