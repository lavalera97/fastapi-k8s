#!/bin/bash

echo "Creating volume and volume claim..."
kubectl apply -f ./k8s/persistent-volume.yaml
kubectl apply -f ./k8s/persistent-volume-claim.yaml

echo "Creating secrets and configmap..."
kubectl apply -f ./k8s/postgres-config.yaml
kubectl apply -f ./k8s/postgres-secret.yaml
kubectl apply -f ./k8s/webapp-secret.yaml

echo "Creating database..."
kubectl apply -f ./k8s/postgres-deploy.yaml

echo "Creating webapp..."
kubectl apply -f ./k8s/webapp-deploy.yaml

echo "Creating ingress..."
kubectl apply -f ./k8s/webapp-ingress.yaml

echo "Creating migration"
kubectl apply -f ./k8s/migration-job.yaml
