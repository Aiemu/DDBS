echo 'Installing python packages...'
python -m pip install -r requirements.txt

echo 'Setting up mongodb...'
docker-compose -f docker/mongo-docker-compose.yml up -d
mongo mongodb://localhost:27600 docker/scripts/configsvr.js
mongo mongodb://localhost:27700 docker/scripts/shard0.js
mongo mongodb://localhost:27711 docker/scripts/shard1.js
mongo mongodb://localhost:27701 docker/scripts/shardrep.js
mongo mongodb://localhost:27500 docker/scripts/router.js
python init_db.py

echo 'Setting up redis...'
docker-compose -f docker/redis-docker-compose.yml up -d
cat docker/scripts/redis.txt | redis-cli -h <PRIVATE_IP> -p 6379

echo 'Setting up hadoop...'
docker build -t hadoop:3.2.1 .
chmod +x docker/scripts/init_hdfs.sh
./docker/scripts/init_hdfs.sh

echo 'Starting backend...'
python app.py runserver