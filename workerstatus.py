import redis
import time

redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)

def mark_tasks_failed(worker_id):
    # Find all tasks marked as in-progress by the inactive worker
    task_keys = redis_client.keys("task:*")
    for task_key in task_keys:
        task_status = redis_client.hget(task_key, "status")
        task_worker_id = redis_client.hget(task_key, "worker_id")
        
        if task_status == "in-progress" and task_worker_id == worker_id:
            # Mark task as failed
            redis_client.hset(task_key, "status", "FAILED")
            redis_client.hset(task_key, "error", f"Worker {worker_id} became inactive")
            print(f"Marked task {task_key} as FAILED due to inactive worker {worker_id}")

def get_worker_status(threshold_seconds=5):
    current_time = time.time()
    active_workers = []
    inactive_workers = []
    worker_keys = redis_client.keys("worker:*:heartbeat")
    
    for key in worker_keys:
        worker_id = key.split(":")[1]
        last_heartbeat = float(redis_client.get(key))
        time_diff = current_time - last_heartbeat
        
        if time_diff < threshold_seconds:
            active_workers.append(worker_id)
        else:
            inactive_workers.append(worker_id)
            mark_tasks_failed(worker_id)
    
    return active_workers, inactive_workers

def monitor_workers():
    print("Starting Worker Monitoring...")
    while True:
        active_workers, inactive_workers = get_worker_status(threshold_seconds=15)
        print("\n==============================")
        print("Active Workers:", active_workers)
        print("Inactive Workers:", inactive_workers)
        print("==============================")
        time.sleep(5)

if __name__ == "__main__":
    monitor_workers()

