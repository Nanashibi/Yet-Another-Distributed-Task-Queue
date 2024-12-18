import yadtq
import redis 
import json
import uuid
import time

yadtq.config(backend = "localhost:6379")
client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)
#'task_5': yadtq.send_task('sub', ["we",2])
task_ids = {
    'task_1': yadtq.send_task('mul', [3, 5]),
    'task_2': yadtq.send_task('add', [8, 9]),
    'task_3': yadtq.send_task('sub', [7, 6]),
    'task_4': yadtq.send_task('mul', [9, 2]),
    'task_5': yadtq.send_task('div', [9, 0]),
    'task_6': yadtq.send_task('add', [1, 2]),
    'task_7': yadtq.send_task('sub', [3, 2]),
    'task_8': yadtq.send_task('div', [7, 3]),
    'task_9': yadtq.send_task('sub', [8, 3]),
    'task_10': yadtq.send_task('sub', [9, 3])
    
}

task_status = {}

while any(task_status.get(task_name) != 'SUCCESS' for task_name in task_ids):
    for task_name, task_id in task_ids.items():
        current_status = yadtq.get_status(task_id)
        
        if current_status != task_status.get(task_name):
            task_status[task_name] = current_status
            print(f"{task_name} ({task_id}) status: {current_status}")
            
            if current_status == 'SUCCESS':
                result = yadtq.get_result(task_id)
                print(f"{task_name} ({task_id}) result: {result}")
            if current_status == 'FAILED':
                error = yadtq.get_result(task_id)
                print(f"{task_name} ({task_id}) error: {error}")

    time.sleep(1)
