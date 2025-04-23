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

        stage('Test') {
            steps {
                sh '''
                    . venv/bin/activate
                    robot --outputdir reports tests/
                '''
            }
        }

        stage('Report') {
            steps {
                sh '''
                    . venv/bin/activate
                    ${PYTHON} scripts/traceability.py > reports/traceability.json
                '''
                junit 'reports/output.xml'
                archiveArtifacts artifacts: 'reports/**'
            }
        }
    }

    post {
        always {
            echo "✅ Build finished. Cleaning up if needed."
        }
    }
}
