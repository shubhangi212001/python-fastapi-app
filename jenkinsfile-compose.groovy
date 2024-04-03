pipeline {
    agent any 
    
    environment {
        GITHUB_CREDENTIALS = credentials('github-credentials')
        GITHUB_USERNAME = 'github-credentials.username'
        GITHUB_PASSWORD = 'github-credentials.password'
    }
    stages {
        stage('Workspace Cleaning'){
            steps{
                cleanWs()
            }
        }
        stage("Code"){
            steps{
                git url: "https://github.com/shubhangi212001/python-fastapi-app.git", branch: "main"
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying the container'
                sh "docker-compose down && docker compose up"
            }
        }
    }
}