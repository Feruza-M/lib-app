pipeline {
    agent any

    environment {
        APP_SERVER = '54.242.16.246'
        SSH_KEY = '/var/lib/jenkins/.ssh/lib-app-key.pem'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t lib-app:latest .'
            }
        }

        stage('Deploy to Application Server') {
            steps {
                sh '''
                ssh -o StrictHostKeyChecking=no -i ${SSH_KEY} ubuntu@${APP_SERVER} "mkdir -p ~/lib-app"

                scp -o StrictHostKeyChecking=no -i ${SSH_KEY} \
                  Dockerfile \
                  docker-compose.yml \
                  requirements.txt \
                  env.example \
                  ubuntu@${APP_SERVER}:~/lib-app/

                scp -o StrictHostKeyChecking=no -i ${SSH_KEY} -r \
                  app \
                  ubuntu@${APP_SERVER}:~/lib-app/

                ssh -o StrictHostKeyChecking=no -i ${SSH_KEY} ubuntu@${APP_SERVER} '
                    cd ~/lib-app &&
                    docker compose down || true &&
                    docker compose build &&
                    docker compose up -d
                '
                '''
            }
        }

        stage('Health Check') {
            steps {
                sh '''
                sleep 10
                curl --fail http://${APP_SERVER}:8000/health
                '''
            }
        }
    }
}
