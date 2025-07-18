from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from datetime import datetime
import os

# 🔹 Initialize Flask app first
app = Flask(__name__, static_folder="build", static_url_path="/")
CORS(app)

LOG_FILE = "ip-log.txt"

# 🔹 API route to log IP from frontend fetch()
@app.route("/api/log-ip", methods=["POST"])
def log_ip():
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} - {ip} (manual POST)\n"
    with open(LOG_FILE, "a") as f:
        f.write(log_entry)
    return jsonify({"status": "logged"}), 200

# 🔹 Serve React frontend and log all requests
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_react_app(path):
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    if path == "":
        label = "home"
    elif os.path.exists(os.path.join(app.static_folder, path)):
        label = f"static file: {path}"
    else:
        label = "unmatched route"

    log_entry = f"{timestamp} - {ip} ({label})\n"
    with open(LOG_FILE, "a") as f:
        f.write(log_entry)

    if path == "" or not os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, "index.html")
    else:
        return send_from_directory(app.static_folder, path)

# 🔹 Start server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

