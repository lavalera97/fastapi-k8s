#!/bin/bash

echo "Deleting everything from k8s..."
kubectl delete -f ./k8s/
