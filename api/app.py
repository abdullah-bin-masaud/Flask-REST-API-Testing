"""
REST API for Telemetry, System Health, and Device Operations.
Provides endpoints for health checking, live telemetry, device management, and hardware command actuation.
"""
import time
from datetime import datetime
from flask import Flask, jsonify, request

app = Flask(__name__)
START_TIME = time.time()
command_log = []


@app.route("/api/status", methods=["GET"])
def get_status():
    uptime = time.time() - START_TIME
    return jsonify({
        "status": "online",
        "service": "telecom-telemetry-gateway",
        "version": "1.2.0",
        "uptime_seconds": round(uptime, 2),
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }), 200


@app.route("/api/telemetry", methods=["GET"])
def get_telemetry():
    return jsonify({
        "temperature": 24.8,
        "humidity": 51.5,
        "cpu_load": 36.2,
        "voltage": 5.02,
        "current_ma": 420.0,
        "status": "nominal",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }), 200


@app.route("/api/command", methods=["POST"])
def post_command():
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 400

    data = request.get_json()
    command = data.get("command")
    valid_commands = ["start", "stop", "reset", "calibrate"]

    if not command or command not in valid_commands:
        return jsonify({
            "error": "Invalid or missing command",
            "allowed_commands": valid_commands
        }), 400

    command_log.append({"command": command, "timestamp": time.time()})
    return jsonify({
        "result": "acknowledged",
        "command": command,
        "execution_state": "queued"
    }), 200


@app.route("/api/stream/frame", methods=["GET"])
def get_stream_frame():
    return jsonify({
        "frame_id": int(time.time() * 10) % 100000,
        "resolution": "640x480",
        "encoding": "MJPEG",
        "fps_target": 30,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }), 200


@app.route("/api/devices", methods=["GET"])
def list_devices():
    return jsonify({
        "count": 2,
        "devices": [
            {"id": "DEV-001", "name": "ESP32 Sensor Node", "status": "active"},
            {"id": "DEV-002", "name": "Raspberry Pi 4B Gateway", "status": "active"}
        ]
    }), 200


@app.route("/api/log", methods=["DELETE"])
def clear_log():
    command_log.clear()
    return "", 204


@app.errorhandler(404)
def handle_404(e):
    return jsonify({"error": "Resource not found", "status_code": 404}), 404


@app.errorhandler(405)
def handle_405(e):
    return jsonify({"error": "Method not allowed", "status_code": 405}), 405


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
