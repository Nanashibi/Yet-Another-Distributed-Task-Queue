import json
import logging
import time
import redis
from kafka import KafkaProducer, KafkaConsumer
import uuid

producer = None
consumer = None
redis_client = None

def config(backend="localhost:6379", group_id=None):
    global consumer, producer, redis_client
    producer = KafkaProducer(value_serializer=lambda m: json.dumps(m).encode('utf-8'))
    
    consumer = KafkaConsumer(
        "yadtq",
        group_id=group_id,
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        auto_offset_reset="earliest",
        session_timeout_ms=10000,
        heartbeat_interval_ms=3000
    )
    
    host, port = backend.split(":")
    redis_client = redis.Redis(host=host, port=int(port))
    return True

def get_status(task_id):
    status = redis_client.hget(f'task:{task_id}', 'status')
    if status:
        return status.decode('utf-8')
    else:
        return "NOT_FOUND"

def get_result(task_id):
    while True:
        result = redis_client.hget(f'task:{task_id}', 'result')
        status = get_status(task_id)
        
        if status == 'SUCCESS' and result:
            return json.loads(result.decode('utf-8'))
        
        if status == 'FAILED':
            error = redis_client.hget(f'task:{task_id}', 'error')
            return Exception(error if error else 'Task failed')
            

def send_task(task_name, args=None):
    if args is None:
        args = []
    
    task_id = str(uuid.uuid4())
    task = {"id": task_id, "task": task_name, "args": args}
    
    producer.send('yadtq', task)
    producer.flush()
    
    redis_client.hset(f'task:{task_id}', 'status', 'queued')
    
    return task_id

def get_messages():
    return consumer

def update_status(task_id, status, result=None, error=None):
    update_dict = {'status': status}
    if result is not None:
        update_dict['result'] = json.dumps(result)
    if error is not None:
        update_dict['error'] = error
    redis_client.hset(f'task:{task_id}', mapping=update_dict)
