import time
import threading
from queue import Queue

# Simulate message queue
data_queue = Queue()

# Simulate Temperature sensors
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

# Start sensor data reading thread
threading.Thread(target=read_sensor_data, daemon=True).start()

# Initialize database
conn = sqlite3.connect("sensor_data.db", check_same_thread=False)
c = conn.cursor()
c.execute()