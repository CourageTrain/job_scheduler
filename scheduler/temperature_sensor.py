import time
import threading
from queue import Queue

data_queue = Queue()

sensors = {
    "sensor_1":{"temperature": 22.5, "last_active": time.time()},
    "sensor_2":{"temperature": 22.5, "last_active": time.time()}
}

def read_temperature():
    while True:
        for sensor in sensors:
            sensors["temperature"]+=0.1
            sensors["last_active"] += time.time()
            data_queue.put((sensor_id, sensor["temperature"], sensor["last_active"]))
        time.sleep(1)

threading.Thread(target=read_sensor_data, daemon=True).start()