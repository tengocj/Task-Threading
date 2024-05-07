import threading
import queue
import random
import time

class WorkerThread(threading.Thread):
    def __init__(self, thread_id, key_queue):
        super().__init__()
        self.thread_id = thread_id
        self.key_queue = key_queue

    def run(self):
        while True:
            try:
                # Try to get a key from the queue with a timeout
                pool_key = self.key_queue.get(timeout=3)
                # Simulate some processing by sleeping
                processing_time = random.uniform(0.5, 2.0)
                print(f"Thread {self.thread_id} processing key '{pool_key}' for {processing_time:.2f} seconds.")
                time.sleep(processing_time)
                self.key_queue.task_done()  # Mark the task as done
            except queue.Empty:
                # If no keys are left to process, exit the loop
                print(f"Thread {self.thread_id} found no keys left and is terminating.")
                break

# Generate a queue of keys
key_queue = queue.Queue()
keys = [f'key{i}' for i in range(1, 11)]
for key in keys:
    key_queue.put(key)

threads = [WorkerThread(i, key_queue) for i in range(5)]

for thread in threads:
    thread.start()

# Wait for all items in the queue to be processed
key_queue.join()

# Wait for all threads to complete (they will terminate after the queue is empty)
for thread in threads:
    thread.join()

print("All threads have completed their tasks.")
