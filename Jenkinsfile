pipeline {
    agent any

    environment {
        // Credentials will be injected via withCredentials
        INFLUXDB_HOST     = 'localhost'  // Replace with actual host or use credentials
        INFLUXDB_PORT     = '8086'
        INFLUXDB_DB       = 'cpap_tests'
        GRAFANA_URL      = 'http://localhost:3000'  // Replace with actual URL
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
                withCredentials([
                    string(credentialsId: 'GRAFANA_API_KEY', variable: 'GRAFANA_API_KEY'),
                    string(credentialsId: 'INFLUXDB_USER', variable: 'INFLUXDB_USER'),
                    string(credentialsId: 'INFLUXDB_PASSWORD', variable: 'INFLUXDB_PASSWORD')
                ]) {
                    sh '''
                        . venv/bin/activate
                        python3 scripts/traceability.py > reports/traceability.json
                        python3 scripts/send_to_influx_v1.py reports/output.xml
                    '''
                }
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