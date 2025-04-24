pipeline {
    agent any

    environment {
        PYTHON = 'python3'
        ROBOT = 'robot'
        PATH = "${env.HOME}/Library/Python/3.9/bin:$PATH"
        INFLUXDB_HOST = 'localhost'
        INFLUXDB_PORT = '3000'
        INFLUXDB_DB = 'cpap_tests'
        GRAFANA_API_KEY = credentials('grafana-api-key')
    }

    triggers {
        githubPush()
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
                    pip install influxdb requests
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
                    ${PYTHON} scripts/send_to_influx_v1.py reports/output.xml
                '''
                archiveArtifacts artifacts: 'reports/**'
            }
        }

        stage('Grafana Annotation') {
            steps {
                script {
                    def result = currentBuild.currentResult
                    def dashboardUrl = "http://your-grafana-host:3000/d/your-dashboard-id"
                    
                    sh """
                    . venv/bin/activate
                    ${PYTHON} -c "
import requests
import os
headers = {
    'Authorization': f'Bearer {env.GRAFANA_API_KEY}',
    'Content-Type': 'application/json'
}
data = {
    'text': f'Build {env.BUILD_NUMBER} {result}',
    'tags': ['jenkins', '${env.JOB_NAME}', result.toLowerCase()],
    'dashboardId': 'your-dashboard-id'
}
response = requests.post(
    'http://your-grafana-host:3000/api/annotations',
    json=data,
    headers=headers
)
print(f'Grafana annotation status: {response.status_code}')
                    "
                    """
                }
            }
        }
    }

    post {
        always {
            echo "✅ Build finished. Cleaning up if needed."
        }
    }
}