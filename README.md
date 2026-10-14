# Security Log Analyzer — CI/CD Pipeline & Kubernetes Deployment

**Continuous Competency Assessment 2 (CCA 2)**  
*TYCSE · Cloud Computing and DevOps Laboratory*  
**Repository**: [https://github.com/Vedant056/log-analyzer](https://github.com/Vedant056/log-analyzer)

---

## 1. Project Overview

The **Security Log Analyzer** is a Python cybersecurity tool and web dashboard designed to parse SSH authentication logs (e.g., `/var/log/auth.log`) and detect suspicious access patterns, repeated failed login attempts, and potential brute-force attacks.

### Key Capabilities
- **Regex-based IP Parsing**: Extracts source IP addresses from failed authentication records (`Failed password for ... from <IP>`).
- **Threshold Analysis**: Categorizes IPs based on attempt frequencies:
  - `>= 5 attempts`: `[BRUTE FORCE]` (high severity)
  - `>= 3 attempts`: `[SUSPICIOUS]` (medium severity)
  - `< 3 attempts`: `[NORMAL]` (low severity)
- **Interactive Web Dashboard**: Built using Flask (`app.py`), presenting analysis statistics, timestamps, and detection tables in a clean, responsive interface.
- **Dual Mode**: Can be executed directly as a command-line script (`python3 Log_Analyzer.py`) or as a containerized web service.

---

## 2. CI/CD Pipeline Architecture

```
+-----------------------------------------------------------------------------------------+
|                                CI/CD Pipeline Architecture                              |
+-----------------------------------------------------------------------------------------+

  +---------------+       +------------------+       +-------------------+
  |   Developer   | ----> | GitHub Repository| ----> | Jenkins Automation|
  |  Local / Mac  |  git  |   (log-analyzer) |webhook|  Server (AWS EC2) |
  +---------------+  push +------------------+ /poll +---------+---------+
                                                               |
                                +------------------------------+
                                |
                                v
               +----------------------------------+
               | Stage 1: SCM Checkout            |
               | Stage 2: Build & Syntax Test     |
               | Stage 3: Docker Image Build      |
               | Stage 4: ECR Login & Tagging     |
               | Stage 5: Push to Amazon ECR      |
               | Stage 6: Minikube Deployment     |
               | Stage 7: Workload Verification   |
               +----------------+-----------------+
                                |
                                v
                 +------------------------------+
                 |   Amazon Elastic Container   |
                 |      Registry (AWS ECR)      |
                 |  (student-service:latest)    |
                 +--------------+---------------+
                                |
                                v pull image
                 +------------------------------+
                 |    Minikube Kubernetes Node  |
                 |  - Pod: log-analyzer (x2)    |
                 |  - Svc: NodePort (30080)     |
                 +--------------+---------------+
                                |
                                v
                 +------------------------------+
                 |  Browser / Client Dashboard  |
                 |  http://<minikube-ip>:30080  |
                 +------------------------------+
```

---

## 3. Pipeline Stages & Descriptions

1. **SCM Checkout**: Clones the latest commit from the `main` branch of the GitHub repository.
2. **Build and Test**: Validates dependencies (`Flask`) and executes syntax/compilation checks using `python3 -m py_compile Log_Analyzer.py app.py` to prevent broken code from being packaged.
3. **Docker Build**: Packages the application into a Docker container image based on `python:3.11-slim` using the project's `Dockerfile`.
4. **ECR Login & Tag**: Authenticates the Docker client with the AWS ECR registry (`ap-south-1`) via AWS CLI, and tags the local image with the remote repository URI.
5. **Push to Amazon ECR**: Pushes the tagged image (`220147487089.dkr.ecr.ap-south-1.amazonaws.com/student-service:latest`) to the Amazon ECR private repository.
6. **Minikube Deployment**: Applies declarative Kubernetes manifests (`k8s/deployment.yaml` and `k8s/service.yaml`).
7. **Verification**: Checks pod health, replica count, and NodePort service status.

---

## 4. Setup & Deployment Instructions

### A. Local Execution (CLI & Web)
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run CLI analyzer
python3 Log_Analyzer.py

# 3. Run Flask web dashboard
python3 app.py
# Access dashboard at http://localhost:5000
```

### B. Docker Containerization
```bash
# Build Docker image
docker build -t log-analyzer:latest .

# Run container
docker run -d --name log-analyzer-test -p 5000:5000 log-analyzer:latest

# Access at http://localhost:5000
```

### C. Amazon ECR Integration
```bash
# Authenticate with Amazon ECR
aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin 220147487089.dkr.ecr.ap-south-1.amazonaws.com

# Tag image
docker tag log-analyzer:latest 220147487089.dkr.ecr.ap-south-1.amazonaws.com/student-service:latest

# Push image
docker push 220147487089.dkr.ecr.ap-south-1.amazonaws.com/student-service:latest
```

### D. Kubernetes Deployment on Minikube
```bash
# Start Minikube cluster
minikube start --driver=docker

# Apply Kubernetes manifests
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

# Verify pods and services
kubectl get pods -l app=log-analyzer
kubectl get svc log-analyzer-service

# Access service in browser
minikube service log-analyzer-service
```

---

## 5. Demonstration of Code Change (Version 1 to Version 2)

As required by Section 1 of the CCA 2 Student Guide:
1. **Version 1**: Baseline dashboard displaying standard security metrics and detection summaries.
2. **Version 2**: Update `app.py` with an upgraded header badge (`Version 2.0 - Active Monitoring`).
3. Commit and push the modification to GitHub:
   ```bash
   git add app.py
   git commit -m "feat: release version 2.0 with active monitoring badge"
   git push origin main
   ```
4. Trigger the Jenkins pipeline again to build, tag, and publish the updated image.
5. Verify the rolling update on Minikube and refresh the browser to confirm the live Version 2 deployment.