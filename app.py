# app.py
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuration for SQLite database (replace with your own database URL)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///devices.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Device model representing the device table in the database
class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    integration_key = db.Column(db.String(255), nullable=False, unique=True)
    user_id = db.Column(db.Integer, nullable=False)  # Assuming a user ID is associated with the device

# Data model representing the historical data table in the database
class HistoricalData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'), nullable=False, index=True)
    timestamp = db.Column(db.DateTime, nullable=False, index=True)
    value = db.Column(db.Float, nullable=False)
# Dashboard model representing the dashboard table in the database
class Dashboard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    devices = db.relationship('Device', secondary='dashboard_device_association', lazy='subquery', backref=db.backref('dashboards', lazy=True))
    data = db.Column(db.String(255), nullable=False)

# Association table for the many-to-many relationship between Dashboard and Device
dashboard_device_association = db.Table('dashboard_device_association',
    db.Column('dashboard_id', db.Integer, db.ForeignKey('dashboard.id')),
    db.Column('device_id', db.Integer, db.ForeignKey('device.id'))
)

# Create the database tables
db.create_all()

# ... (existing code)

# API endpoint to create a new dashboard
@app.route('/api/create_dashboard', methods=['POST'])
def create_dashboard():
    try:
        # Get data from the request
        data = request.json
        dashboard_name = data.get('name')
        selected_devices = data.get('selectedDevices', [])
        selected_data = data.get('selectedData')

        # Validate the request data
        if not dashboard_name or not selected_devices or not selected_data:
            raise ValueError("Dashboard name, selected devices, and selected data are required.")

        # Create a new dashboard instance
        new_dashboard = Dashboard(name=dashboard_name, data=selected_data)

        # Add selected devices to the new dashboard
        for device_id in selected_devices:
            device = Device.query.get(device_id)
            if device:
                new_dashboard.devices.append(device)

        # Add the new dashboard to the database
        db.session.add(new_dashboard)
        db.session.commit()

        # Return the newly created dashboard in the response
        return jsonify({"id": new_dashboard.id, "name": new_dashboard.name, "data": new_dashboard.data}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400

# ... (existing code)

# ... (existing code)

# API endpoint to add a new device
@app.route('/api/add_device', methods=['POST'])
def add_device():
    try:
        # Get data from the request
        data = request.json
        device_name = data.get('name')
        integration_key = data.get('integrationKey')
        user_id = data.get('userId')  # Adjust this based on your authentication system

        # Validate the request data
        if not device_name or not integration_key or not user_id:
            raise ValueError("Device name, integration key, and user ID are required.")

        # Create a new device instance
        new_device = Device(name=device_name, integration_key=integration_key, user_id=user_id)

        # Add the new device to the database
        db.session.add(new_device)
        db.session.commit()

        # Return the newly created device in the response
        return jsonify({"id": new_device.id, "name": new_device.name, "integrationKey": new_device.integration_key}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400

# ... (existing code)
# ... (existing code)

# Route to serve the documentation page
@app.route('/documentation')
def documentation():
    return render_template('documentation.html')

# ... (existing code)
# API endpoint to retrieve historical data for a specific device
@app.route('/api/retrieve_historical_data', methods=['POST'])
def retrieve_historical_data():
    try:
        # Get data from the request
        data = request.json
        device_id = data.get('deviceID')
        time_range = data.get('timeRange')

        # Validate the request data
        if not device_id or not time_range:
            raise ValueError("Device ID and time range are required.")

        # Implement logic to query historical data from the database based on device ID and time range
        # For simplicity, this example returns dummy data
        dummy_data = [
            {"timestamp": "2023-01-01T12:00:00", "value": 30.5},
            {"timestamp": "2023-01-01T13:00:00", "value": 31.2},
            # Add more data points as needed
        ]

        return jsonify(dummy_data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

# ... (existing code)
# API endpoint to save notification settings
@app.route('/api/save_notification_settings', methods=['POST'])
def save_notification_settings():
    try:
        # Get data from the request
        data = request.json
        enable_critical_event_notifications = data.get('enableCriticalEventNotifications')

        # Implement logic to save notification settings to the database or another storage

        return jsonify({"message": "Notification settings saved successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

# ... (existing code)