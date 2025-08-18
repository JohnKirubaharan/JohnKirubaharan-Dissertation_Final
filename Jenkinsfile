pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/YOUR_USERNAME/YOUR_REPO.git'
            }
        }
        stage('Build & Deploy') {
            steps {
                sh '''
                docker-compose down || true
                docker-compose up -d --build
                '''
            }
        }
    }
}
