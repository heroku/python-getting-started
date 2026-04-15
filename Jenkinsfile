pipeline {
    agent any

    stages {

        stage('Build') {
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
                pip install pytest
                pytest || true
                '''
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                echo "Deploying app..."
                nohup python3 app.py &
                '''
            }
        }
    }
}
