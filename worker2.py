import time
import yadtq
import redis
import json
import threading
global result

redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)
worker_id = 2

yadtq.config(backend="localhost:6379", group_id="worker")

def add(a, b):
    time.sleep(5)
    return a + b

def sub(a, b):
    time.sleep(10)
    return a - b

def mul(a, b):
    time.sleep(15)
    return a * b
    
def div(a, b):
    time.sleep(10)
    return a / b	

TASK_FUNCTIONS = {"add": add, "sub": sub, "mul": mul, "div": div}

def send_heartbeat():
    while True:
        redis_client.set(f'worker:{worker_id}:heartbeat', time.time())
        print(f"Worker {worker_id} heartbeat sent.")
        time.sleep(5)  

heartbeat_thread = threading.Thread(target=send_heartbeat, daemon=True)
heartbeat_thread.start()
while True:
    print(f"Worker {worker_id} Active ... \n")
    for message in yadtq.get_messages():
        task_data = message.value
        task_id = task_data["id"]
        task_name = task_data["task"]
        task_args = task_data["args"]

        # Check task status before processing
        current_status = yadtq.get_status(task_id)
        if current_status == "SUCCESS":
            print ("skipping", current_status)
            continue

        print(f"Received task: {task_name} with id: {task_id} (Status: {current_status})")

        try:
            yadtq.update_status(task_id, 'in-progress')
            redis_client.hset(f"task:{task_id}", "worker_id", worker_id)
            
            func = TASK_FUNCTIONS[task_name]
            result = func(*task_args)
            print("Result: ", result)
            
            yadtq.update_status(task_id, 'SUCCESS', result=result)
            print(f"Task {task_id} completed successfully")
            print("---------------------------------------------------------------------------------------------------------------")
        except Exception as e:
            print(f"Task {task_id} failed: {e}")
            yadtq.update_status(task_id, 'FAILED', error=str(e))
    
    time.sleep(5)



