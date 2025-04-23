pipeline {
    agent any
    
    environment {
        PYTHON = 'python3'
        ROBOT = 'robot'
        PATH = "${env.HOME}/Library/Python/3.9/bin:$PATH"
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
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install -r requirements.txt
                '''
    }

        }
        
        steps {
        sh '''
            . venv/bin/activate
            robot --outputdir reports tests/
        '''
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
    
   
}