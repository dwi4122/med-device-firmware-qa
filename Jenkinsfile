pipeline {
    agent any
    
    environment {
        PYTHON = 'python3'
        ROBOT = 'robot'
    }
    
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                url: 'https://github.com/dwi4122/med-device-firmware-qa.git'
            }
        }
        
        stage('Setup') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }
        
        stage('Test') {
            steps {
                sh '$ROBOT --outputdir reports tests/'
            }
        }
        
        stage('Report') {
            steps {
                robot outputPath: 'reports/output.xml'
                junit 'reports/output.xml'
                
                // Generate traceability report
                sh '$PYTHON scripts/traceability.py > reports/traceability.json'
                
                // Archive results
                archiveArtifacts artifacts: 'reports/**'
            }
        }
    }
    
    post {
        always {
            // Notify stakeholders
            emailext body: '${currentBuild.currentResult}: ${env.JOB_NAME} #${env.BUILD_NUMBER}\n\nResults: ${env.BUILD_URL}testReport',
            subject: 'Medical Device Test Results',
            to: 'qa-team@example.com'
        }
    }
}