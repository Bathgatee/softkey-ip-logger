from flask import Flask, request
from flask_cors import CORS, cross_origin
from datetime import datetime

app = Flask(__name__)
CORS(app)  # still keep this, but use decorator too

LOG_FILE = "ip-log.txt"

@app.route("/api/log-ip", methods=["POST"])
@cross_origin(origin="http://localhost:5173")  # ✅ Allow only your React dev server
def log_ip():
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} - {ip}\n"
    with open(LOG_FILE, "a") as f:
        f.write(log_entry)
    return {"status": "logged"}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
