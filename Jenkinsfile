pipeline {
    agent any

    environment {
        ECR_URL_MONGODB = "587447957359.dkr.ecr.us-east-1.amazonaws.com/portfolio-mongodb"
        ECR_URL_FRONTEND = "587447957359.dkr.ecr.us-east-1.amazonaws.com/portfolio-frontend"
        ECR_URL_BACKEND = "587447957359.dkr.ecr.us-east-1.amazonaws.com/portfolio-backend"
        DOCKER_NETWORK = 'jenkins_nw'
        AWS_REGION = "us-east-1"
        IMAGE_TAG = "1.0.0"

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
                }
            }
        }
        stage('Run Images') {
            steps {
                // Build Docker image
                script {
                    docker.image('mongodb-test').run("--rm --name mongodb_jenkins_test --network internal_tests -p 27017:27017 --env-file .env")
                    //waitForMongoDB() adding `--link mongo:mongo` is the alternative for the healthcheck function to mongo
                    docker.image('backend-test').run("--rm --name backend_jenkins_test -m 2g --memory-swap 2g -p 5000:5000 --network internal_tests --network ${DOCKER_NETWORK} --env-file .env --link mongodb_jenkins_test:mongodb")
                    docker.image('frontend-test').run("--rm --name frontend_jenkins_test -p 80:80 --network ${DOCKER_NETWORK} --network internal_tests")

                }
            }
        }
        stage('unit Tests') {
            steps {
                script {                 
                    sh 'docker exec backend_jenkins_test pytest -s -v test_app.py'
                }
            }
        }

        stage('E2E Tests') {
            steps {
                script {                 
                    sh './e2e_tests/tests.sh'
                }
            }
            post {
                always {
                    // Remove Docker container after test stage
                    script {
                        sh 'docker stop mongodb_jenkins_test'
                        sh 'docker stop frontend_jenkins_test'
                        sh 'docker stop backend_jenkins_test'
                        
                    }
                }
            }
        }
        stage('Deploy backend') {
            when {
                anyOf {
                    changeset "src/**"
                    expression {
                        return sh(script: 'git diff --name-only HEAD~1 HEAD | grep -q "^\\.env" || echo "no"', returnStatus: true) == 0
                    }
                    not {
                        expression {
                            return sh(script: "aws ecr describe-images --repository-name portfolio-backend --image-ids imageTag=1.0.0 --region ${AWS_REGION}", returnStatus: true) == 0
                        }
                    }         
                }
            }
            steps {
                script {
                    IMAGE_TAG = sh (script: "aws ecr list-images --repository-name portfolio-backend --filter --region ${AWS_REGION} tagStatus=TAGGED | grep imageTag | awk ' { print \$2 } ' |sort -V -r | head -1 | sed 's/\"//g' |tr \".\" \" \" | awk ' { print \$1 \".\" \$2 \".\" \$3+1 } '", returnStdout: true).trim()                  
                    if (IMAGE_TAG == ""){
                        IMAGE_TAG = "1.0.0"
                    }
                    sh "aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_URL_BACKEND}"
                    def image = docker.build("portfolio-backend", '-f Dockerfile.backend .')
                    docker.withRegistry("https://${ECR_URL_BACKEND}", '') {
                        image.push("${IMAGE_TAG}")
                    }
                }
            }
        }
        stage('Deploy frontend') {
            when {
                anyOf {
                    changeset "frontend/**"                   
                    not {
                        expression {
                            return sh(script: "aws ecr describe-images --repository-name portfolio-frontend --image-ids imageTag=${IMAGE_TAG} --region ${AWS_REGION}", returnStatus: true) == 0
                        }
                    }         
                }
            }
            steps {
                script {
                    IMAGE_TAG = sh (script: "aws ecr list-images --repository-name portfolio-frontend --filter --region ${AWS_REGION} tagStatus=TAGGED | grep imageTag | awk ' { print \$2 } ' |sort -V -r | head -1 | sed 's/\"//g' |tr \".\" \" \" | awk ' { print \$1 \".\" \$2 \".\" \$3+1 } '", returnStdout: true).trim()
                    if (IMAGE_TAG == ""){
                        IMAGE_TAG = "1.0.0"
                    }
                    sh "aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_URL_FRONTEND}"
                    def image = docker.build("portfolio-frontend", '-f Dockerfile.frontend .')
                    docker.withRegistry("https://${ECR_URL_FRONTEND}", '') {
                        image.push("${IMAGE_TAG}")
                    }
                }
            }
        }
        stage('Deploy Mongodb') {
            when {
                anyOf {
                    changeset "initdb.d/**"      
                    expression {
                        return sh(script: 'git diff --name-only HEAD~1 HEAD | grep -q "^\\.env" || echo "no"', returnStatus: true) == 0
                    }             
                    not {
                        expression {
                            return sh(script: "aws ecr describe-images --repository-name portfolio-mongodb --image-ids imageTag=${IMAGE_TAG} --region ${AWS_REGION}", returnStatus: true) == 0
                        }
                    }         
                }
            }
            steps {
                script {
                    IMAGE_TAG = sh (script: "aws ecr list-images --repository-name portfolio-mongodb --filter --region ${AWS_REGION} tagStatus=TAGGED | grep imageTag | awk ' { print \$2 } ' |sort -V -r | head -1 | sed 's/\"//g' |tr \".\" \" \" | awk ' { print \$1 \".\" \$2 \".\" \$3+1 } '", returnStdout: true).trim()
                    if (IMAGE_TAG == ""){
                        IMAGE_TAG = "1.0.0"
                    }
                    sh "aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_URL_MONGODB}"
                    def image = docker.build("portfolio-mongodb", '-f Dockerfile.mongodb .')
                    docker.withRegistry("https://${ECR_URL_MONGODB}", '') {
                        image.push("${IMAGE_TAG}")
                    }
                }
            }
        }
    }
    post { 
        always { 
            cleanWs()
        }
        failure {
            script {
                try {
                    sh 'docker stop mongodb_jenkins_test'
                } catch (Exception e) {
                    echo "mongodb container crushed."
                }

                try {
                    sh 'docker stop frontend_jenkins_test'
                } catch (Exception e) {
                    echo "frontend container crushed."
                }

                try {
                   sh 'docker stop backend_jenkins_test'
                } catch (Exception e) {
                    echo "backend container crushed."
                }
            }
        }
    }
}


    

def waitForMongoDB() {
    def maxRetries = 30
    def retryInterval = 2 // seconds

    for (int i = 0; i < maxRetries; i++) {
        def exitCode = sh(returnStatus: true, script: "docker exec mongodb_jenkins_test mongosh --eval 'db.adminCommand({ ping: 1 })'")

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