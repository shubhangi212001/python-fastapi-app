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


# Deploy application using kubernetes

$kubectl apply -f deployment.yml   -------- this is the deployment file of kubernetes
$kubectl get deployments   ------ list all deployments
$kubectls get pods  ---------- list all pods
$kubectl get svc   --------list all services


 
 












 
