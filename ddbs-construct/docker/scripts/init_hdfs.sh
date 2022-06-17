docker network create --driver=bridge hadoop
docker run -itd --net=hadoop -p 9870:9870 -p 8088:8088 --name hadoop-master --hostname hadoop-master hadoop:3.2.1

N=${1:-3}
i=1
while [ $i -lt $N ]
do
    docker run -itd --net=hadoop --name hadoop-slave$i --hostname hadoop-slave$i hadoop:3.2.1
    i=$(( $i + 1 ))
done

docker exec -it hadoop-master bash -c 'start-all.sh && hdfs dfs -mkdir -p articles && hdfs dfs -put ./articles/* articles'