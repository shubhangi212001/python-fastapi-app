pipeline {
    agent any

    environment {
        GITLAB_CREDENTIALS = credentials('gitlab-credentials')
        GITLAB_USERNAME = 'gitlab-credentials.username'
        GITLAB_PASSWORD = 'gitlab-credentials.password'
    }
    stages {
        stage('Workspace Cleaning'){
            steps{
                cleanWs()
            }
        }
        stage("Code"){
            steps{
                git credentialsId: 'gitlab-credentials', url: "https://gitlab360.enlight.dev/shubhangishinde/python-fastapi-app.git", branch: "main"
            }
        }
        stage('Deploying App to Kubernetes') {
      steps {
        script {
          kubernetesDeploy(configs: "deployment.yml", kubeconfigId: "kubernetes", deleteAction: true)
          kubernetesDeploy(configs: "deployment.yml", kubeconfigId: "kubernetes")
          kubernetesDeploy(configs: "service.yml", kubeconfigId: "kubernetes")
        }
      }
    }
     
    }
    post {
        always {
            emailext attachLog: true,
                subject: "'${currentBuild.result}'",
                body: "Project: ${env.JOB_NAME}<br/>" +
                    "Build Number: ${env.BUILD_NUMBER}<br/>" +
                    "URL: ${env.BUILD_URL}<br/>",
                to: 'shubhangi.shinde@esds.co.in',
        }
    }
}
