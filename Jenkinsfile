pipeline {
    agent any

    environment {
        GRAFANA_API_KEY   = credentials('GRAFANA_API_KEY')
        INFLUXDB_HOST     = credentials('NFLUXDB_HOST')
        INFLUXDB_PORT     = credentials('INFLUXDB_PORT')
        INFLUXDB_DB       = credentials('INFLUXDB_DB')
        INFLUXDB_USER     = credentials('influx-user')
        INFLUXDB_PASSWORD = credentials('influx-password')
        GRAFANA_URL       = credentials('GRAFANA_URL')
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
                    pip install --upgrade pip
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
                    python3 scripts/traceability.py > reports/traceability.json
                    python3 scripts/send_to_influx_v1.py reports/output.xml
                '''
                archiveArtifacts artifacts: 'reports/**'
            }
        }

        stage('Grafana Annotation') {
            steps {
                script {
                    def result = currentBuild.currentResult
                    sh """
                        . venv/bin/activate
                        python3 -c "
import requests
import os
headers = {
    'Authorization': f'Bearer {os.environ['GRAFANA_API_KEY']}',
    'Content-Type': 'application/json'
}
data = {
    'text': f'Build ${env.BUILD_NUMBER} ${result}',
    'tags': ['jenkins', '${env.JOB_NAME}', '${result}'.lower()],
}
response = requests.post(
    '${env.GRAFANA_URL}/api/annotations',
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
