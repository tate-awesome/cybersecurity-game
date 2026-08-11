"""
Flask host server for ESP32 REST API — Defender dashboard.

Run:
    pip install flask
    python Host_API.py

Open http://localhost:5000
"""

from flask import Flask, request, jsonify, Response
from datetime import datetime
from collections import deque

app = Flask(__name__)

# ─── DATA STORE ────────────────────────────────────────────────────────────
MAX_POINTS         = 100
client_log         = deque(maxlen=MAX_POINTS)   # packets from Client ESP32
server_log         = deque(maxlen=MAX_POINTS)   # packets from Server ESP32
pending_set_x      = None
client_total       = 0
server_total       = 0
encryption_status  = False
encryption_key     = ""


# ─── HELPERS ───────────────────────────────────────────────────────────────

def _parse_packet(packet: dict, seq: int) -> dict:
    return {
        "seq":         seq,
        "timestamp":   packet["timestamp"],
        "x":           packet["x"],
        "y":           packet.get("y",      0.0),
        "theta":       packet.get("theta",  0.0),
        "speed":       packet.get("speed",  0.0),
        "rudder":      packet.get("rudder", 0.0),
        "received_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


# ─── ROUTES ────────────────────────────────────────────────────────────────

@app.route("/")
def dashboard():
    """Minimal status page — the full UI lives in the Python desktop app."""
    html = """<!DOCTYPE html>
<html><head><title>ESP32 Host</title>
<style>body{font-family:monospace;background:#0a0f14;color:#c8dde8;padding:40px}</style>
</head><body>
<h2 style="color:#00c8e0">ESP32 Host Server</h2>
<p>Server is running. Use the Defender GUI to monitor data.</p>
<p><a href="/api/data" style="color:#00e5aa">View /api/data</a></p>
</body></html>"""
    return Response(html, mimetype="text/html")


@app.route("/data", methods=["POST"])
def receive_data():
    """
    Accepts telemetry from either ESP32.
    Caller should pass  source="client"  or  source="server"  in the JSON body.
    Defaults to "client" for backwards compatibility with the original Client.ino.
    """
    global pending_set_x, client_total, server_total, encryption_status

    if not request.is_json:
        return jsonify({"error": "Expected JSON"}), 400

    packet = request.get_json()
    if "timestamp" not in packet or "x" not in packet:
        return jsonify({"error": "Missing fields"}), 422

    source = packet.get("source", "client").lower()

    if source == "server":
        server_total += 1
        entry = _parse_packet(packet, server_total)
        server_log.append(entry)
    else:
        client_total += 1
        entry = _parse_packet(packet, client_total)
        client_log.append(entry)

    now = datetime.now().strftime("%H:%M:%S")
    print(
        f"[{now}] [{source.upper()}]"
        f"  seq={entry['seq']}"
        f"  x={entry['x']:.3f}  y={entry['y']:.3f}"
        f"  theta={entry['theta']:.4f} rad"
        f"  speed={entry['speed']:.3f} m/s"
        f"  rudder={entry['rudder']:.2f} deg"
        f"  ENC={'ON' if encryption_status else 'OFF'}"
        + (f"  KEY={encryption_key!r}" if encryption_key else "")
    )

    response = {
      "status":            "ok",
      "encryption_status": encryption_status,
      "encryption_key":    encryption_key,
      "target_x":          target_x,
      "target_y":          target_y,
    }
    if pending_set_x is not None:
        response["set_x"] = pending_set_x
        print(f"  --> Sending command: set_x = {pending_set_x}")
        pending_set_x = None

    return jsonify(response), 200


@app.route("/set_encryption", methods=["POST"])
def set_encryption():
    global encryption_status, encryption_key
    if not request.is_json:
        return jsonify({"error": "Expected JSON"}), 400
    body = request.get_json()
    if "encryption_status" not in body:
        return jsonify({"error": "Missing encryption_status field"}), 422

    encryption_status = bool(body["encryption_status"])
    encryption_key    = str(body.get("encryption_key", encryption_key))

    print(
        f"  --> encryption_status={'ON' if encryption_status else 'OFF'}"
        + (f"  key={encryption_key!r}" if encryption_key else "")
    )
    return jsonify({
        "encryption_status": encryption_status,
        "encryption_key":    encryption_key,
    }), 200

target_x = 100.0
target_y = 100.0

@app.route("/set_target", methods=["POST"])
def set_target():
    global target_x, target_y
    data = request.get_json()
    target_x = float(data.get("target_x", target_x))
    target_y = float(data.get("target_y", target_y))
    return jsonify({"status": "ok"})
    
@app.route("/api/data", methods=["GET"])
def api_data():
    """
    Returns separate client_points and server_points lists so the Defender
    GUI can display them independently.  Also keeps a combined 'points' key
    for any backwards-compatible consumers.
    """
    combined = list(client_log)   # map always driven by client
    resp = jsonify({
        "client_points":     list(client_log),
        "server_points":     list(server_log),
        "points":            combined,          # backwards compat
        "client_total":      client_total,
        "server_total":      server_total,
        "total_count":       client_total,      # backwards compat
        "encryption_status": encryption_status,
        "encryption_key":    encryption_key,
        "target_x": target_x,
        "target_y": target_y,
    })
    resp.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"
    resp.headers["Pragma"]        = "no-cache"
    resp.headers["Expires"]       = "0"
    return resp, 200


@app.route("/command", methods=["POST"])
def send_command():
    global pending_set_x
    if not request.is_json:
        return jsonify({"error": "Expected JSON"}), 400
    cmd = request.get_json()
    if "set_x" in cmd:
        pending_set_x = float(cmd["set_x"])
        return jsonify({"queued": True, "set_x": pending_set_x}), 200
    return jsonify({"error": "Unknown command"}), 400


@app.route("/status", methods=["GET"])
def status():
    return jsonify({
        "server":            "running",
        "pending_set_x":     pending_set_x,
        "encryption_status": encryption_status,
        "encryption_key":    encryption_key,
        "client_total":      client_total,
        "server_total":      server_total,
    }), 200


# ─── ENTRY POINT ───────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("ESP32 host server starting on http://0.0.0.0:5000")
    print("  GET  /                 <- status page")
    print("  POST /data             <- ESP32 posts here (source=client|server)")
    print("  GET  /api/data         <- GUI polls here")
    print("  POST /command          <- send set_x command")
    print("  POST /set_encryption   <- set encryption_status + key")
    app.run(host="0.0.0.0", port=5000, debug=True)