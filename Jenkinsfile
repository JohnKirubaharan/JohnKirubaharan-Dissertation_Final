pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/JohnKirubaharan/JohnKirubaharan-Dissertation_Final.git'
            }
        }
        stage('Build & Deploy') {
            steps {
                sh '''
                docker-compose down || true
                docker rm -f flask_app || true
                docker-compose up -d --build
                '''
            }
        }
    }
}

go to Jenkins
login with username and password

admin
admin

error happened because im already running 