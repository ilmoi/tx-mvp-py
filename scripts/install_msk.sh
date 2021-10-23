# install awscli
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
sudo apt install unzip
unzip awscliv2.zip
sudo ./aws/install
echo PATH=/usr/local/bin/aws:$PATH >> ~/.bashrc
aws --version

# install java
sudo apt update
sudo apt install default-jre
java --version

# get kafka
wget https://archive.apache.org/dist/kafka/2.6.2/kafka_2.12-2.6.2.tgz
tar -zxf kafka_2.12-2.6.2.tgz
cd kafka_2.12-2.6.2

# create topic
bin/kafka-topics.sh --create --zookeeper "z-2.sol-cluster-2.k4mb5d.c18.kafka.us-east-1.amazonaws.com:2181,z-1.sol-cluster-2.k4mb5d.c18.kafka.us-east-1.amazonaws.com:2181,z-3.sol-cluster-2.k4mb5d.c18.kafka.us-east-1.amazonaws.com:2181" --replication-factor 3 --partitions 1 --topic cities2

# start producer
#bin/kafka-console-producer.sh --broker-list "b-3.sol-cluster-2.k4mb5d.c18.kafka.us-east-1.amazonaws.com:9092,b-1.sol-cluster-2.k4mb5d.c18.kafka.us-east-1.amazonaws.com:9092,b-2.sol-cluster-2.k4mb5d.c18.kafka.us-east-1.amazonaws.com:9092" --producer.config config/producer.properties --topic cities2

# start consumer
#bin/kafka-console-consumer.sh --bootstrap-server "b-3.sol-cluster-2.k4mb5d.c18.kafka.us-east-1.amazonaws.com:9092,b-1.sol-cluster-2.k4mb5d.c18.kafka.us-east-1.amazonaws.com:9092,b-2.sol-cluster-2.k4mb5d.c18.kafka.us-east-1.amazonaws.com:9092" --consumer.config config/consumer.properties --topic cities2 --from-beginning

