import threading
from queue import Queue
import time

print_lock = threading.Lock()

def exampleJob(worker):
    time.sleep(0.5)
    
    print_lock.acquire()
    print(threading.current_thread().name, "worker: ", worker)
    print_lock.release()

def threader():
    while True:
        worker = q.get()
        exampleJob(worker)
        q.task_done()

q = Queue()

# creating 10 Threads
for x in range(10):
    t = threading.Thread(target=threader)
    t.daemon = True
    t.start()

# 20 jobs
for worker in range(20):
    q.put(worker)

q.join()

start = time.time()
print("Done in : ", time.time()-start)
    

