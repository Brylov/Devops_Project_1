pipeline {
    agent any

    environment {
        DOCKER_NETWORK = 'jenkins_nw'
    }
    
    stages {
        stage('Decrypt Files') {
            steps {
                withCredentials([string(credentialsId: 'decryption-key', variable: 'DECRYPTION_KEY')]) {
                    script {
                        sh "openssl enc -aes-256-cbc -d -in .env.enc -out .env -k '$DECRYPTION_KEY'"
                        sh "openssl enc -aes-256-cbc -d -in initdb.d/init-mongo.js.enc -out initdb.d/init-mongo.js -k '$DECRYPTION_KEY'"
                    }
                }
            }
        }
        stage('Build Images') {
            steps {
                // Build Docker image
                script {
                    docker.build('backend-test', '-f Dockerfile.backend .')
                    docker.build('frontend-test', '-f Dockerfile.frontend .')
                    docker.build('mongodb-test', '-f Dockerfile.mongodb .')
                    //sh "docker run --rm --name portfolio-translator --network jenkins_nw -d translator-test"
                }
            }
        }
        stage('Run Images') {
            steps {
                // Build Docker image
                script {
                    sh 'docker network create internal_tests'
                    def mongoContainer = docker.image('mongodb-test').run("--rm --name mongodb_jenkins_test --network internal_tests -p 27017:27017 --env-file .env")
                    waitForMongoDB(mongoContainer)
                    docker.image('backend-test').run("--rm --name backend_jenkins_test -p 5000:5000  --network internal_tests --env-file .env")
                    docker.image('frontend-test').run("--rm --name frontend_jenkins_test -p 80:80 --network ${DOCKER_NETWORK} --network internal_tests")
                    // Load environment variables from .env file
                    // Run MongoDB container with environment variables              
                    //sh "docker run --rm --name portfolio-translator --network jenkins_nw -d translator-test"

                }
            }
        }
        stage('unit Tests') {
            steps {
                script {                 
                    // Run pytest inside the Docker container
                    sh 'docker exec backend_jenkins_test pytest -s -v test_app.py'
                }
            }
        }

        stage('E2E Tests') {
            steps {
                script {                 
                    // Run pytest inside the Docker container
                    sh 'docker exec translator_jenkins_test pytest'
                }
            }
            post {
                always {
                    // Remove Docker container after test stage
                    script {
                        sh 'docker stop mongodb_jenkins_test'
                        sh 'docker stop backend_jenkins_test'
                        sh 'docker stop frontend_jenkins_test'
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
            script{
                sh 'docker stop mongodb_jenkins_test'
                sh 'docker stop backend_jenkins_test'
                sh 'docker stop frontend_jenkins_test'
                sh 'docker network rm internal_tests'

            }
        }
    }
}
def waitForMongoDB() {
    def maxRetries = 30
    def retryInterval = 10 // seconds

    for (int i = 0; i < maxRetries; i++) {
        def exitCode = sh(returnStatus: true, script: "docker exec -it mongodb_jenkins_test mongo --eval 'db.adminCommand(\"ping\")'")

        if (exitCode == 0) {
            echo "MongoDB is ready!"
            return
        } else {
            echo "MongoDB is not yet ready. Retrying in ${retryInterval} seconds..."
            sleep(retryInterval)
        }
    }

    error("Failed to start MongoDB container or MongoDB is not ready after ${maxRetries} retries.")
}