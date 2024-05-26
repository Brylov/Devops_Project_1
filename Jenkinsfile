pipeline {
    agent any
    
    stages {
        stage('Build') {
            steps {
                // Replace this with your build steps
                sh 'echo "Building..."'
            }
        }
        stage('Test') {
            steps {
                // Replace this with your test steps
                sh 'echo "Testing..."'
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
            // Cleanup steps that should always run, regardless of success or failure
            sh 'echo "Cleaning up..."'
        }
        success {
            // Actions to perform if the pipeline succeeds
            sh 'echo "Pipeline succeeded!"'
        }
        failure {
            // Actions to perform if the pipeline fails
            sh 'echo "Pipeline failed!"'
        }
    }
}