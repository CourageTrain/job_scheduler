def process_data():
    while True:
        if not data_queue.empty():
            sensor_id, temperature, timestamp = data_queue.get()
            store_sensor_data(sensor_id, temperature, timestamp)

threading.Thread(target=process_data, daemon=True).start()