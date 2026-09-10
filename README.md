# Flask Kubernetes Sprint 🚀

A production-style DevOps project demonstrating containerization, Kubernetes deployment, persistent storage, secrets/configuration management, health probes, CI/CD automation, and failure recovery.

## 📌 Project Overview

This project deploys a Flask application on Kubernetes with MySQL as the database.

The application is:

- Containerized using Docker
- Stored on Docker Hub
- Deployed on a Minikube Kubernetes cluster running on AWS EC2
- Connected to MySQL using Kubernetes Service discovery
- Configured using ConfigMap and Secret
- Protected with persistent storage using PVC
- Configured with readiness and liveness probes
- Automatically tested and deployed using GitHub Actions

---

## 🏗️ Architecture

```text
                         GitHub
                           |
                           v
                  GitHub Actions CI/CD
                           |
             +-------------+-------------+
             |                           |
             v                           v
        Run Tests                 Build Docker Image
             |                           |
             |                           v
             |                    Docker Hub
             |                           |
             +-------------+-------------+
                           |
                           v
                      SSH to EC2
                           |
                           v
                    Minikube Cluster
                           |
                    flask-sprint Namespace
                           |
             +-------------+-------------+
             |                           |
             v                           v
      Flask Backend                 MySQL Database
        2 Replicas                    1 Replica
             |                           |
             |                           v
             |                       MySQL PVC
             |
             v
      Flask Backend Service
          NodePort 30080
             |
             v
           Client
🛠️ Technologies Used
Technology	Purpose
Python	Application development
Flask	Backend framework
Gunicorn	Production WSGI server
Docker	Application containerization
Docker Hub	Container image registry
Kubernetes	Container orchestration
Minikube	Kubernetes cluster
AWS EC2	Server environment
MySQL 8	Database
ConfigMap	Non-sensitive configuration
Secret	Database credentials
PVC	Persistent database storage
Git	Version control
GitHub	Source code repository
GitHub Actions	CI/CD automation
kubectl	Kubernetes management
Linux/Ubuntu	Server environment
📁 Project Structure
flask-kubernetes-sprint/
│
├── app.py
├── Dockerfile
├── requirements.txt
├── .dockerignore
├── .gitignore
├── README.md
│
├── tests/
│   └── test_app.py
│
├── .github/
│   └── workflows/
│       └── ci-cd.yml
│
└── k8s/
    ├── namespace.yaml
    ├── configmap.yaml
    ├── secret-example.yaml
    ├── pvc.yaml
    ├── deployment.yaml
    ├── service.yaml
    ├── backend-deployment.yaml
    └── backend-service.yaml

k8s/secret.yaml contains local credentials and is intentionally excluded from Git using .gitignore.

🐍 Flask Application

The Flask application provides the following endpoints.

Home
GET /
Hello
GET /hello
Health
GET /health

Used by Kubernetes readiness and liveness probes.

Database Health
GET /db-health

Tests connectivity between Flask and MySQL.

Example:

{
    "status": "healthy",
    "database": "connected"
}
🐳 Docker
Build Image
docker build -t flask-kubernetes-sprint:v2 .
Run Container
docker run -d \
  --name flask-app \
  -p 5000:5000 \
  flask-kubernetes-sprint:v2
Test
curl http://localhost:5000/health
☁️ Docker Hub

Docker Hub repository:

poonamrajore/flask-kubernetes-sprint

Docker images are tagged using Git commit SHA values in the CI/CD pipeline.

☸️ Kubernetes Deployment
Start Minikube
minikube start --driver=docker

Check cluster:

kubectl get nodes
Create Namespace
kubectl apply -f k8s/namespace.yaml
Create ConfigMap
kubectl apply -f k8s/configmap.yaml
Create Secret

The real Secret is intentionally excluded from Git.

kubectl apply -f k8s/secret.yaml
Create PVC
kubectl apply -f k8s/pvc.yaml
Deploy MySQL
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
Deploy Flask Backend
kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/backend-service.yaml
🔍 Health Checks

The Flask Deployment uses Kubernetes readiness and liveness probes.

Readiness Probe
readinessProbe:
  httpGet:
    path: /health
    port: 5000

Determines whether the Pod is ready to receive traffic.

Liveness Probe
livenessProbe:
  httpGet:
    path: /health
    port: 5000

Allows Kubernetes to detect an unhealthy application.

🔗 Application Testing

Get the Service URL:

minikube service flask-backend-service -n flask-sprint --url

Test the application:

curl http://127.0.0.1:<PORT>/

Test health:

curl http://127.0.0.1:<PORT>/health

Test database connectivity:

curl http://127.0.0.1:<PORT>/db-health

Expected:

{
    "status": "healthy",
    "database": "connected"
}
🔄 CI/CD Pipeline

GitHub Actions automates the deployment process.

Git Push
   |
   v
Checkout Code
   |
   v
Install Dependencies
   |
   v
Run Pytest
   |
   v
Build Docker Image
   |
   v
Push Image to Docker Hub
   |
   v
SSH to EC2
   |
   v
Apply Kubernetes Manifests
   |
   v
Update Backend Image
   |
   v
Rollout Verification

Workflow:

.github/workflows/ci-cd.yml
🔐 GitHub Actions Secrets

The following GitHub repository secrets are used:

DOCKERHUB_USERNAME
DOCKERHUB_TOKEN
EC2_HOST
EC2_USER
EC2_SSH_KEY

Secrets are never hard-coded into the workflow.

🧪 Testing

Tests are located in:

tests/test_app.py

Run locally:

pytest

Expected:

2 passed

Tests are automatically executed by GitHub Actions before Docker image creation.

💥 Failure Simulation

A backend failure was simulated by scaling the Deployment to zero replicas:

kubectl scale deployment flask-backend --replicas=0 -n flask-sprint

Verify:

kubectl get pods -n flask-sprint

The Flask Pods become unavailable.

🔧 Recovery

Restore the backend replicas:

kubectl scale deployment flask-backend --replicas=2 -n flask-sprint

Verify:

kubectl get pods -n flask-sprint

Check rollout:

kubectl rollout status deployment/flask-backend -n flask-sprint

Expected:

deployment "flask-backend" successfully rolled out

This demonstrates Kubernetes desired-state management and recovery.

🐛 Troubleshooting Commands
Check all resources
kubectl get all -n flask-sprint
Check Pods
kubectl get pods -n flask-sprint
Pod logs
kubectl logs <pod-name> -n flask-sprint
Describe Pod
kubectl describe pod <pod-name> -n flask-sprint
Check Deployment
kubectl get deployment -n flask-sprint
Check Services
kubectl get services -n flask-sprint
Check PVC
kubectl get pvc -n flask-sprint
Check rollout
kubectl rollout status deployment/flask-backend -n flask-sprint
Check ReplicaSets
kubectl get replicasets -n flask-sprint
📊 Observability & Reliability

The project demonstrates:

Readiness probe
Liveness probe
Multiple backend replicas
Persistent MySQL storage
Kubernetes Service discovery
Resource requests and limits
Deployment rollout verification
Failure simulation and recovery
Automated CI/CD validation
🚀 Final Deployment State
Namespace: flask-sprint

Flask Backend:
  Replicas: 2
  Status: Running

MySQL:
  Replicas: 1
  Status: Running

Backend Service:
  Type: NodePort
  Port: 30080

MySQL Service:
  Type: ClusterIP
  Port: 3306

MySQL Storage:
  PVC: mysql-pvc
  Size: 2Gi
🎯 Sprint Outcome

This project demonstrates an end-to-end DevOps workflow:

Application Development
        ↓
GitHub
        ↓
Automated Testing
        ↓
Docker Build
        ↓
Docker Hub
        ↓
Kubernetes Deployment
        ↓
Health Checks
        ↓
Database Connectivity
        ↓
Failure Simulation
        ↓
Recovery
👩‍💻 Author

Poonam Chauhan

DevOps / Cloud Engineering Project

Technologies: AWS EC2, Linux, Docker, Kubernetes, MySQL, GitHub Actions, Docker Hub
