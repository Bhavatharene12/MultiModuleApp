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
        DOCKER = 'C:\\Users\\bhava\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker.exe'
        KUBECTL = 'C:\\Users\\bhava\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\kubectl.exe'
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

                    echo "Branch : ${branch}"
                    echo "Building Version : v${env.VER}"
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
                    run "\"${env.DOCKER}\" build --build-arg VERSION=${env.VER} -t ${env.IMAGE_NAME}:v${env.VER} ."
                }
            }
        }

        stage('Docker Login') {
            steps {
                script {
                    if (isUnix()) {
                        sh 'echo $DOCKERHUB_PSW | docker login -u $DOCKERHUB_USR --password-stdin'
                    } else {
                        bat 'echo %DOCKERHUB_PSW% | "C:\\Users\\bhava\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker.exe" login -u %DOCKERHUB_USR% --password-stdin'
                    }
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    run "\"${env.DOCKER}\" push ${env.IMAGE_NAME}:v${env.VER}"
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script {
                    run "\"${env.KUBECTL}\" apply -f deployment-v${env.VER}.yaml"
                    run "\"${env.KUBECTL}\" apply -f service-v${env.VER}.yaml"
                    run "\"${env.KUBECTL}\" rollout restart deployment/multimoduleapp-v${env.VER}"
                }
            }
        }

        stage('Verify Deployment') {
            steps {
                script {
                    run "\"${env.KUBECTL}\" get deployments"
                    run "\"${env.KUBECTL}\" get services"
                    run "\"${env.KUBECTL}\" get pods"
                }
            }
        }
    }

    post {
        success {
            echo "========================================"
            echo "Pipeline completed successfully!"
            echo "Version : v${env.VER}"
            echo "Image   : ${env.IMAGE_NAME}:v${env.VER}"
            echo "URL     : http://localhost:3000${env.VER}"
            echo "========================================"
        }

        failure {
            echo "Pipeline failed. Check the Console Output."
        }
    }
}