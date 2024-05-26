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
                    docker.image('translator-test').run("--name translator_jenkins_test --network jenkins_nw")                  
                    // Run pytest inside the Docker container
                    sh 'docker exec translator_jenkins_test pytest'
                }
            }
            post {
                always {
                    // Remove Docker container after test stage
                    script {
                        docker.container('translator_jenkins_test').remove()
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