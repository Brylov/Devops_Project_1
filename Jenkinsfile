pipeline {
    agent any
    
    stages {
        stage('Build && Run') {
            steps {
                // Build Docker image
                script {
                    docker.build('translator-test')
                    //sh "docker run --rm --name portfolio-translator --network jenkins_nw -d translator-test"
                }
            }

        }
        stage('Test') {
            steps {
                script {
                    def dockerImage = docker.image('translator-test').run("--network jenkins_nw")                  
                    // Run pytest inside the Docker container
                    dockerImage.inside() {
                        sh 'pytest'
                    }
                }
            }
            post {
                always {
                    // Remove Docker container after test stage
                    script {
                        docker.image('translator-test').remove()
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