@echo off
REM Deploys all three versions to Kubernetes (Docker Desktop)
for %%n in (1 2 3) do (
  kubectl apply -f deployment-v%%n.yaml
  kubectl apply -f service-v%%n.yaml
)
kubectl get deployment
kubectl get all
