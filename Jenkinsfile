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
         stage('Build') {
            steps {
                echo 'Building the image'
                sh "docker build -t fastapi-py-app ."
            }
        }
        stage('Push') {
            steps {
                echo 'Pushing docker image on Docker Hub'
                withCredentials([usernamePassword(credentialsId: 'DOCKERHUB', passwordVariable: 'dockerHubpass', usernameVariable: 'dockerHubuser')]) {
                    sh "docker tag fastapi-py-app ${env.dockerHubuser}/fastapi-py-app:latest"
                    sh "docker login -u ${env.dockerHubuser} -p ${env.dockerHubpass}"
                    sh "docker push ${env.dockerHubuser}/fastapi-py-app:latest"
                }
            }
        }
       
        stage('Deploy to Kubernetes'){
            steps{
                script{
                    
                        withKubeConfig(caCertificate: '', clusterName: '', contextName: '', credentialsId: 'k8s_122', namespace: '', restrictKubeConfigAccess: false, serverUrl: '') {
                                sh 'kubectl delete -f deployment.yml'
                                sh 'kubectl delete -f service.yml'
                                sh 'kubectl apply -f deployment.yml'
                                sh 'kubectl apply -f service.yml'
                                sh 'kubectl get svc'
                                sh 'kubectl get all'
                        }   
                    
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
                to: 'shubhangi.shinde@esds.co.in'
        }
    }
}
