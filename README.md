# EC-Team-28-yadtq-yet-another-distributed-task-queue-

### Things to do before you actually run this thing
- Start Kafka: `sudo systemctl start kafka`
- Convert the script file into executable: `chmod +x yadtqsetup.sh`
- Run the script file: `./yadtqsetup.sh`
- Start Redis: `sudo systemctl start redis`


### Things you can do
- Details about task queue
`/../usr/local/kafka/bin/kafka-topics.sh --describe --topic yadtq --bootstrap-server localhost:9092`

- Monitor consumer group activity and lag
`/../usr/local/kafka/bin/kafka-consumer-groups.sh --describe --group "worker" --bootstrap-server localhost:9092`

### Okay, how to actually run it?
- Run each of these on different terminals
`python3 worker1.py`
`python3 worker2.py`
`python3 worker3.py`
`python3 client.py`
- Additionally, to check the status of the workers, run this command on a different terminal `python3 workerstatus.py`
