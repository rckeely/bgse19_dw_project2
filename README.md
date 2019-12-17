# bgse19_dw_project2
Repository for Data Warehousing Project 2 (Shirley / Ben / Richie)

### Application Overview
This application uses a convex optimiser to calculate the odds for an NFL survivor pool, [ https://survivor.fantasy.nfl.com/ ]. It consists of a single Docker container that contains the Dash frontend, the custom Python backend as well as a gevent server.

### Setup Overview
This project was hosted on the same server as the first project. To recap, in order to setup the system, we used Docker. To install:

``` shell
wget https://get.docker.com/
mv index.html getDocker.sh
chmod 744 getDocker.sh
sh getDocker.sh
sudo usermod -aG docker ubuntu
# Then reload user account
```

Because of the size of the `cvxpy` library, it did not seem feasible to build the container on the AWS instance. Instead, it was built locally and pushed to Docker Hub.

On the local system:
``` shell
docker build -t rckeely/dw2_flask .
docker login
docker push rckeely/dw2_flask
```

On the remote system:
``` shell
docker pull rckeely/dw2_flask:latest
docker run -d --name dw2_flask -p 80:5000 rckeely/dw2_flask
```
