from flask import Flask, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def dashboard():
    return render_template("dashboard.html")

@app.route('/sensor_data')
def get_sensor_data():
    c.execute("SELECT * FROM sensor_data")
    data = c.fetchall()
    return jsonify(data)

@app.route('/sensor_health')
def get_sensor_health():
    c.execute("SELECT * FROM sensor_health")
    health = c.fetchall()
    return jsonify(health)

if __name__=="__main__":
    app.run(debug=True)