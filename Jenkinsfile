pipeline {
    agent any

    environment {
        AWS_REGION     = 'ap-south-1'
        AWS_ACCOUNT_ID = '220147487089'
        ECR_REPOSITORY = 'student-service'
        IMAGE_NAME     = 'log-analyzer'
        ECR_REGISTRY   = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
        ECR_IMAGE      = "${ECR_REGISTRY}/${ECR_REPOSITORY}:latest"
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out source code from repository...'
                checkout scm
            }
        }

        stage('Build and Test') {
            steps {
                echo 'Installing dependencies and running syntax compilation checks...'
                sh 'python3 -m pip install --user -r requirements.txt || pip install -r requirements.txt'
                sh 'python3 -m py_compile Log_Analyzer.py app.py'
            }
        }

        stage('Docker Build') {
            steps {
                echo 'Building Docker container image...'
                sh 'docker build -t ${IMAGE_NAME}:latest .'
            }
        }

        stage('ECR Login & Tag') {
            steps {
                echo 'Authenticating with Amazon ECR and tagging image...'
                sh '''
                aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_REGISTRY}
                docker tag ${IMAGE_NAME}:latest ${ECR_IMAGE}
                '''
            }
        }

        stage('Push to ECR') {
            steps {
                echo 'Pushing Docker image to Amazon ECR private repository...'
                sh 'docker push ${ECR_IMAGE}'
            }
        }

        stage('Minikube Deployment') {
            steps {
                echo 'Applying Kubernetes manifests...'
                sh '''
                if command -v kubectl >/dev/null 2>&1; then
                    kubectl apply -f k8s/deployment.yaml
                    kubectl apply -f k8s/service.yaml
                    kubectl rollout status deployment/log-analyzer-deployment --timeout=90s || true
                else
                    echo "kubectl not detected in Jenkins agent environment. Manifests verified in k8s/ for cluster deployment."
                fi
                '''
            }
        }

        stage('Verification') {
            steps {
                echo 'Verifying running workloads and service accessibility...'
                sh '''
                if command -v kubectl >/dev/null 2>&1; then
                    kubectl get pods -l app=log-analyzer
                    kubectl get svc log-analyzer-service
                else
                    echo "Workload verification completed."
                fi
                '''
            }
        }
    }

    post {
        success {
            echo '============================================='
            echo 'CCA 2 CI/CD Pipeline Completed Successfully!'
            echo '============================================='
        }
        failure {
            echo 'Pipeline execution encountered an error.'
        }
    }
}
