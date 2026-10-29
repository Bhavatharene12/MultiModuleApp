// One Jenkinsfile for all versions. The Git branch decides which version is built:
//   branch v1   -> image :v1 -> deployment/service v1 -> port 30001
//   branch v2   -> image :v2 -> deployment/service v2 -> port 30002
//   branch main -> image :v3 -> deployment/service v3 -> port 30003

def run(String cmd) {
    if (isUnix()) {
        sh cmd
    } else {
        bat cmd
    }
}

pipeline {
    agent any

    environment {
        IMAGE_NAME = 'bhavatharene12/multimoduleapp'
        DOCKERHUB = credentials('dockerhub-creds')
        PYTHON = 'C:\\Users\\bhava\\AppData\\Local\\Programs\\Python\\Python313\\python.exe'
    }

    stages {

        stage('Git Checkout') {
            steps {
                checkout scm
                script {
                    def branch = (env.BRANCH_NAME ?: env.GIT_BRANCH ?: 'main').replaceAll('^origin/', '')

                    if (branch == 'v1') {
                        env.VER = '1'
                    } else if (branch == 'v2') {
                        env.VER = '2'
                    } else {
                        env.VER = '3'
                    }

                    echo "Branch: ${branch}"
                    echo "Building Version: v${env.VER}"
                }
            }
        }

        stage('Install Requirements') {
            steps {
                script {
                    if (isUnix()) {
                        sh 'python3 -m pip install -r requirements.txt'
                    } else {
                        bat "\"${env.PYTHON}\" -m pip install -r requirements.txt"
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    run "docker build --build-arg VERSION=${env.VER} -t ${env.IMAGE_NAME}:v${env.VER} ."
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    if (isUnix()) {
                        sh 'echo $DOCKERHUB_PSW | docker login -u $DOCKERHUB_USR --password-stdin'
                    } else {
                        bat 'echo %DOCKERHUB_PSW%| docker login -u %DOCKERHUB_USR% --password-stdin'
                    }

                    run "docker push ${env.IMAGE_NAME}:v${env.VER}"
                }
            }
        }

        stage('Deploy Kubernetes') {
            steps {
                script {
                    run "kubectl apply -f deployment-v${env.VER}.yaml"
                    run "kubectl apply -f service-v${env.VER}.yaml"
                    run "kubectl rollout restart deployment/multimoduleapp-v${env.VER}"
                    run "kubectl get deployment"
                }
            }
        }
    }

    post {
        success {
            echo "===================================="
            echo "Deployment Successful!"
            echo "Version : v${env.VER}"
            echo "URL : http://localhost:3000${env.VER}"
            echo "===================================="
        }

        failure {
            echo "Pipeline failed. Check the console output."
        }
    }
}