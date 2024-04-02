# Run phpmyadmin, mysql database and fastapi app containers

$vim database.py  ---------- change IP address 

$vim main.py  --------------- change IP address

$vim Dockerfile  ------------ change internal port of application if needed

-------------------------------
phpmyadmin
-------------------------------
docker pull phpmyadmin:5.0.2

docker run --name demo1-phpmyadmin -d -p 8067:80 -e PMA_HOST=172.17.0.9:3306 phpmyadmin/phpmyadmin:5.0.2

-------------------------------
mysql
-------------------------------
 
docker run -itd --name demo1_database -e MYSQL_ROOT_PASSWORD=support#123 -p 4806:3306 mysql

docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' 378343673dcd
 
-------------------------------
python 
-------------------------------
docker build -t my-fastapi-app .

docker run -v "$PWD":/dastapp/ -p 8083:8083  --name my-fastapi-app -itd my-fastapi-app
 

# Try all the above things using docker-copmpose 

$docker-compose up  ---- command to deploy application using docker compose

$docker-compose down  ----- command to down docker compose 

# write a jenkins file to do docker-compose using jenkins CI/CD

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
                sh "docker-compose down"
            }
        }
    }
}


# Deploy application using kubernetes

$kubectl apply -f deployment.yml   -------- this is the deployment file of kubernetes

$kubectl apply -f service.yml   ---------- this is a service file to access applications externally

$kubectl get deployments   ------ list all deployments

$kubectls get pods  ---------- list all pods

$kubectl get svc   --------list all services

$kubectl logs -f <pod_name>  --- to check logs of pod

# commands to delete averall kubernetes deployment

$kubectl delete -f deployment.yml

$kubectl delete -f service.yml

 
 












 
