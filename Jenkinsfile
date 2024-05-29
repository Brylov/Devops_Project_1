pipeline {
    agent any
    
    stages {
        stage('Build && Run') {
            steps {
                // Build Docker image
                script {
                    sh 'docker compose -f docker-compose.yaml up -d --build --remove-orphans --force-recreate --network jenkins_nw'
                }
            }

        }
        stage('Test') {
            steps {
                script {
                    sh 'docker ps'
                }
            }
            post {
                always {
                    // Remove Docker container after test stage
                    script {
                        sh 'docker compose down'
                    }
                }
            }
        }
        stage('Deploy') {
            steps {
                // Replace this with your deployment steps
                sh 'echo "Deploying..."'
            }
        }
    }
    
    post { 
        always { 
            cleanWs()
        }
    }
}