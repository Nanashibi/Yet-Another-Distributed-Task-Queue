#!/bin/bash

TOPICS_PATH=$(find /usr -name "kafka-topics.sh" 2>/dev/null | head -n 1)

if [ -z "$TOPICS_PATH" ]; then
    echo "Error: Unable to locate 'kafka-topics.sh'. Please ensure Kafka is installed and available."
    exit 1
fi

echo "Using Kafka topics script: $TOPICS_PATH"

TOPIC_NAME="yadtq"
BOOTSTRAP_SERVER="localhost:9092"
PARTITIONS=3
REPLICATION_FACTOR=1

echo "Installing Redis and its python module..."
sudo apt install redis
pip install redis
echo "Redis installation completed."

echo "Checking if the Kafka topic '$TOPIC_NAME' exists..."
EXISTING_TOPIC=$($TOPICS_PATH --bootstrap-server $BOOTSTRAP_SERVER --list | grep "^$TOPIC_NAME$")

if [ "$EXISTING_TOPIC" ]; then
    echo "Topic '$TOPIC_NAME' exists. Deleting it..."
    $TOPICS_PATH --delete --topic $TOPIC_NAME --bootstrap-server $BOOTSTRAP_SERVER
else
    echo "Topic '$TOPIC_NAME' does not exist. Proceeding to creation..."
fi

echo "Creating the Kafka topic '$TOPIC_NAME'..."
/../$TOPICS_PATH --create --topic $TOPIC_NAME --bootstrap-server $BOOTSTRAP_SERVER --partitions $PARTITIONS --replication-factor $REPLICATION_FACTOR

echo "Kafka topic '$TOPIC_NAME' has been created successfully."
echo "Setup is finished."
