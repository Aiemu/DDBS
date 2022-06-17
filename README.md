# DDBS: A manual

## Introduction
This is a distributed database system based on mongodb, redis and hadoop file system. At the same time, vue and flask are used to realize the front and back ends for the convenience of users. In terms of monitoring, MongoDB Compass and Hadoop Web Page are used to monitor mongodb and hadoop respectively.

## Quick Start
### Prerequisites
- Docker 20.10.16
- MongoDB shell version v5.0.9
- redis-cli 6.2.6
- python 3.8
- node.js 16.9.0
- npm 7.22.0

### One-step Start
You can quickly start by running the command below, or follow the prompts to start step by step (**Note**: Please modify the `privateIP` and `PRIVATE_IP` in the project to your LAN ip before execution).

#### Backend
Execute the following commands in `src/ddbs-construct/`
```bash
chmod +x ddbs.sh
./ddbs.sh
```

#### Frontend
Execute the following commands in `src/ddbs-manage/`
```bash
chmod +x ddbs-manage.sh
./ddbs-manage.sh
```

### Python Package
The pip package required to run the code is installed by executing the following command in the `src`: 
``` bash
python -m pip install -r requirements.txt
```

### Docker Setup
#### MongoDB
First we use docker to start the mongodb cluster, including four shard servers, two config servers and one router server. Execute the following command to start the cluster (**Note**: Please modify the `privateIP` in `docker/mongo-docker-compose.yml` to your LAN ip before execution):

``` bash
docker-compose -f docker/mongo-docker-compose.yml up -d
```

Next, we configure each server separately. First we execute the following command to configure the config server (**Note**: Please modify the `privateIP` in `configsvr.js` to your LAN ip before execution):

```
mongo mongodb://localhost:27600 docker/scripts/configsvr.js
```

After configuring the config server, we execute the following commands to configure four shard servers (**Note**: Please modify the `privateIP` in `shardrep.js` to your LAN ip before execution):

```bash
mongo mongodb://localhost:27700 docker/scripts/shard0.js
mongo mongodb://localhost:27711 docker/scripts/shard1.js
mongo mongodb://localhost:27701 docker/scripts/shardrep.js
```

Finally, let's configure the router server of this mongodb cluster:

```bash
mongo mongodb://localhost:27500 docker/scripts/router.js
```

Through the above steps, we have completed the construction of the mongodb cluster. This cluster includes two databases, DBMS1 and DBMS2, and some backups. The next step is to store the data in the cluster

```
python init_db.py
```

#### Redis
First we start a docker containing redis using the following command
```
docker-compose -f docker/redis-docker-compose.yml up -d
```
Then use the following command to modify the redis configuration (**Note**: Please modify the `PRIVATE_IP` to your LAN ip before execution):
```
cat docker/scripts/redis.txt | redis-cli -h <PRIVATE_IP> -p 6379
```

#### HDFS
Before building the docker image of hdfs, you should first put all the generated articles in the directory `hadoop/articles/`. Then execute the following command to build the docker image of hdfs, which includes two slaves and one master:

```bash
docker build -t hadoop:3.2.1 .
```

Building hadoop can be a lengthy process that can take hours. After the build is complete, execute the following command to create a hadoop cluster

```bash
chmod +x docker/scripts/init_hdfs.sh
./docker/scripts/init_hdfs.sh
```
### Start Backend
Next we start the flask-based backend application with following command:
```bash
python app.py runserver
```
Then, the backend will be started at `http://127.0.0.1:5001`.

### Start Frontend
The front end is done with Vue, first we need to install the dependency library and then start the frontend.
```
cd ../ddbs-manage
npm install
npm run dev
```
Now, you can visit the frontend at `http://127.0.0.1:8080` like this:

![](https://tva1.sinaimg.cn/large/e6c9d24ely1h37qv0ozlfj21tn0u040b.jpg)

### Monitor
We use `mongodb compass` and `hadoop web page` to monitor the status of mongodb and hadoop.

#### Mongodb Compass
![](https://tva1.sinaimg.cn/large/e6c9d24ely1h37rba3rm9j21c00u00x2.jpg)

#### Hadoop Web page
![](https://tva1.sinaimg.cn/large/e6c9d24ely1h37rdis16zj20nu0d2jsf.jpg)
