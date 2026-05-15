"""
Flask host server for ESP32 REST API — simplified dashboard.

Run:
    pip install flask
    python Host_API.py

Open http://localhost:5000  (or http://192.168.8.167:5000 from another device)
"""

from flask import Flask, request, jsonify, Response
from datetime import datetime
from collections import deque

app = Flask(__name__)

# ─── DATA STORE ────────────────────────────────────────────────────────────
MAX_POINTS     = 100
data_log       = deque(maxlen=MAX_POINTS)
pending_set_x  = None
total_received = 0


# ─── DASHBOARD HTML ────────────────────────────────────────────────────────
DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ESP32 Monitor</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: 'Courier New', monospace;
    background: #0a0f14;
    color: #c8dde8;
    display: flex;
    justify-content: center;
    padding: 48px 16px;
    min-height: 100vh;
  }
  .panel {
    width: 100%;
    max-width: 480px;
    display: flex;
    flex-direction: column;
    gap: 24px;
  }
  h1 {
    font-size: 13px;
    letter-spacing: 0.2em;
    color: #00c8e0;
    text-transform: uppercase;
    border-bottom: 1px solid #1a2a36;
    padding-bottom: 12px;
  }
  .block {
    background: #0f1a22;
    border: 1px solid #1a2a36;
    border-radius: 4px;
    padding: 20px;
  }
  .block-label {
    font-size: 10px;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #3a6070;
    margin-bottom: 14px;
  }
  #count {
    font-size: 48px;
    color: #00c8e0;
    line-height: 1;
  }
  #values-list {
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 6px;
  }
  #values-list li {
    display: flex;
    justify-content: space-between;
    font-size: 14px;
    padding: 7px 10px;
    background: #0a0f14;
    border-radius: 3px;
  }
  #values-list li.new { background: #0a2a20; }
  #values-list li .ts  { color: #3a6070; font-size: 12px; }
  #values-list li .val { color: #00e5aa; }
  .cmd-row {
    display: flex;
    gap: 10px;
    align-items: center;
  }
  .cmd-label { font-size: 12px; color: #3a6070; white-space: nowrap; }
  input[type=number] {
    flex: 1;
    background: #0a0f14;
    border: 1px solid #1a2a36;
    border-radius: 3px;
    color: #00c8e0;
    font-family: inherit;
    font-size: 15px;
    padding: 8px 10px;
    outline: none;
  }
  input[type=number]:focus { border-color: #00c8e0; }
  button {
    font-family: inherit;
    font-size: 11px;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding: 8px 16px;
    background: transparent;
    border: 1px solid #00c8e0;
    color: #00c8e0;
    border-radius: 3px;
    cursor: pointer;
    white-space: nowrap;
    transition: background 0.15s, color 0.15s;
  }
  button:hover { background: #00c8e0; color: #0a0f14; }
  #feedback {
    font-size: 11px;
    color: #00e5aa;
    margin-top: 10px;
    min-height: 16px;
    opacity: 0;
    transition: opacity 0.3s;
  }
  #feedback.show { opacity: 1; }
</style>
</head>
<body>
<div class="panel">
  <h1>Defender Monitor</h1>

  <div class="block">
    <div class="block-label">Packets received</div>
    <div id="count">0</div>
  </div>

  <div class="block">
    <div class="block-label">Last 10 x values</div>
    <ul id="values-list"></ul>
  </div>

  <div class="block">
    <div class="block-label">Send command to ESP32</div>
    <div class="cmd-row">
      <span class="cmd-label">set_x =</span>
      <input type="number" id="cmd-x" step="0.1" value="0.0">
      <button onclick="sendCommand()">Send</button>
    </div>
    <div id="feedback">&#10003; queued &mdash; will deliver on next packet</div>
  </div>
</div>

<script>
var lastSeq = -1;

function poll() {
  fetch('/api/data?t=' + Date.now())
    .then(function(r) { return r.json(); })
    .then(function(d) {
      if (!d.points || d.points.length === 0) return;
      var latest = d.points[d.points.length - 1];
      if (latest.seq === lastSeq) return;
      lastSeq = latest.seq;

      document.getElementById('count').textContent = d.total_count;

      var last10 = d.points.slice(-10).reverse();
      var ul = document.getElementById('values-list');
      ul.innerHTML = '';
      last10.forEach(function(p, i) {
        var li = document.createElement('li');
        if (i === 0) li.className = 'new';
        var ts = document.createElement('span');
        ts.className = 'ts';
        ts.textContent = p.received_at.slice(11, 19);
        var val = document.createElement('span');
        val.className = 'val';
        val.textContent = parseFloat(p.x).toFixed(4);
        li.appendChild(ts);
        li.appendChild(val);
        ul.appendChild(li);
      });
    })
    .catch(function(e) { console.warn('poll error', e); });
}

function sendCommand() {
  var val = parseFloat(document.getElementById('cmd-x').value);
  if (isNaN(val)) return;
  fetch('/command', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ set_x: val })
  }).then(function() {
    var fb = document.getElementById('feedback');
    fb.classList.add('show');
    setTimeout(function() { fb.classList.remove('show'); }, 3000);
  });
}

poll();
setInterval(poll, 2000);
</script>
</body>
</html>"""


# ─── ROUTES ────────────────────────────────────────────────────────────────

@app.route("/")
def dashboard():
    return Response(DASHBOARD_HTML, mimetype="text/html")


@app.route("/data", methods=["POST"])
def receive_data():
    global pending_set_x, total_received

    if not request.is_json:
        return jsonify({"error": "Expected JSON"}), 400

    packet = request.get_json()
    if "timestamp" not in packet or "x" not in packet:
        return jsonify({"error": "Missing fields"}), 422

    total_received += 1
    entry = {
        "seq":         total_received,
        "timestamp":   packet["timestamp"],
        "x":           packet["x"],
        "received_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    data_log.append(entry)

    now = datetime.now().strftime("%H:%M:%S")
    print(f"[{now}]  seq={total_received}  timestamp={entry['timestamp']}s   x={entry['x']}")

    response = {"status": "ok"}
    if pending_set_x is not None:
        response["set_x"] = pending_set_x
        print(f"  --> Sending command: set_x = {pending_set_x}")
        pending_set_x = None

    return jsonify(response), 200


@app.route("/api/data", methods=["GET"])
def api_data():
    resp = jsonify({
        "points":      list(data_log),
        "total_count": total_received
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
    return jsonify({"server": "running", "pending_set_x": pending_set_x}), 200


# ─── ENTRY POINT ───────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("ESP32 host server starting on http://0.0.0.0:5000")
    print("  GET  /          <- dashboard")
    print("  POST /data      <- ESP32 posts here")
    print("  GET  /api/data  <- browser polls here")
    print("  POST /command   <- send set_x command")
    app.run(host="0.0.0.0", port=5000, debug=True)