import time
import threading
from queue import Queue
import random
import sqlite3
from flask import Flask, jsonify, render_template

# Simulating a message queue
data_queue = Queue()

# Simulated temperature sensors
sensors = {
    'sensor_1': {'temperature': 22.5, 'last_active': time.time()},
    'sensor_2': {'temperature': 23.0, 'last_active': time.time()},
}

def read_sensor_data():
    while True:
        for sensor_id, sensor in sensors.items():
            # Simulate reading data from the sensor
            sensor['temperature'] += random.uniform(-0.5, 0.5)  # Example temperature change
            sensor['last_active'] = time.time()
            data_queue.put((sensor_id, sensor['temperature'], sensor['last_active']))
            print(f"Sensor {sensor_id} - Temperature: {sensor['temperature']}°C")
        time.sleep(2)  # Polling interval

# Start the sensor data reading thread
threading.Thread(target=read_sensor_data, daemon=True).start()

# Initialize the database
conn = sqlite3.connect('sensor_data.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS sensor_data (sensor_id TEXT, temperature REAL, timestamp REAL)''')
c.execute('''CREATE TABLE IF NOT EXISTS sensor_health (sensor_id TEXT, status TEXT, last_active REAL)''')
conn.commit()

def get_db_connection():
    connection = sqlite3.connect('sensor_data.db', check_same_thread=False)
    connection.row_factory = sqlite3.Row
    return connection

def store_sensor_data(sensor_id, temperature, timestamp):
    conn = get_db_connection()
    c = conn.cursor()
    with conn:
        c.execute("INSERT INTO sensor_data VALUES (?, ?, ?)", (sensor_id, temperature, timestamp))
        c.execute("REPLACE INTO sensor_health VALUES (?, ?, ?)", (sensor_id, 'active', timestamp))
    conn.close()

def check_sensor_health():
    while True:
        current_time = time.time()
        conn = get_db_connection()
        c = conn.cursor()
        for sensor_id in sensors.keys():
            last_active = sensors[sensor_id]['last_active']
            status = 'active' if current_time - last_active < 5 else 'inactive'
            with conn:
                c.execute("REPLACE INTO sensor_health VALUES (?, ?, ?)", (sensor_id, status, last_active))
        conn.close()
        time.sleep(5)

# Start the health monitoring thread
threading.Thread(target=check_sensor_health, daemon=True).start()

def process_data():
    while True:
        if not data_queue.empty():
            sensor_id, temperature, timestamp = data_queue.get()
            print(f"Processing data: {sensor_id}, {temperature}, {timestamp}")
            store_sensor_data(sensor_id, temperature, timestamp)

# Start the data processing thread
threading.Thread(target=process_data, daemon=True).start()

app = Flask(__name__)

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/sensor_data')
def get_sensor_data():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM sensor_data")
    data = c.fetchall()
    conn.close()
    return jsonify([dict(row) for row in data])

@app.route('/sensor_health')
def get_sensor_health():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM sensor_health")
    health = c.fetchall()
    conn.close()
    return jsonify([dict(row) for row in health])

if __name__ == '__main__':
    app.run(debug=True)
