# """
# Flask host server for ESP32 REST API — simplified dashboard.

# Run:
#     pip install flask
#     python Host_API.py

# Open http://localhost:5000  (or http://192.168.8.167:5000 from another device)
# """

# from flask import Flask, request, jsonify, Response
# from datetime import datetime
# from collections import deque

# app = Flask(__name__)

# # ─── DATA STORE ────────────────────────────────────────────────────────────
# MAX_POINTS        = 100
# data_log          = deque(maxlen=MAX_POINTS)
# pending_set_x     = None
# total_received    = 0
# encryption_status = False   # toggled via POST /set_encryption


# # ─── DASHBOARD HTML ────────────────────────────────────────────────────────
# DASHBOARD_HTML = """<!DOCTYPE html>
# <html lang="en">
# <head>
# <meta charset="UTF-8">
# <meta name="viewport" content="width=device-width, initial-scale=1.0">
# <title>CYBERSECURITY DEFENDER Monitor</title>
# <style>
#   * { box-sizing: border-box; margin: 0; padding: 0; }
#   body {
#     font-family: 'Courier New', monospace;
#     background: #0a0f14;
#     color: #c8dde8;
#     display: flex;
#     justify-content: center;
#     padding: 48px 16px;
#     min-height: 100vh;
#   }
#   .panel {
#     width: 100%;
#     max-width: 780px;
#     display: flex;
#     flex-direction: column;
#     gap: 24px;
#   }
#   h1 {
#     font-size: 13px;
#     letter-spacing: 0.2em;
#     color: #00c8e0;
#     text-transform: uppercase;
#     border-bottom: 1px solid #1a2a36;
#     padding-bottom: 12px;
#     display: flex;
#     justify-content: space-between;
#     align-items: center;
#   }
#   #enc-badge {
#     font-size: 11px;
#     letter-spacing: 0.12em;
#     padding: 3px 10px;
#     border-radius: 20px;
#     border: 1px solid #3a6070;
#     color: #3a6070;
#     transition: border-color 0.3s, color 0.3s;
#   }
#   #enc-badge.on { border-color: #00e5aa; color: #00e5aa; }
#   .stats-row {
#     display: grid;
#     grid-template-columns: 1fr 1fr 1fr 1fr 1fr 1fr;
#     gap: 14px;
#   }
#   .block {
#     background: #0f1a22;
#     border: 1px solid #1a2a36;
#     border-radius: 4px;
#     padding: 20px;
#   }
#   .block-label {
#     font-size: 10px;
#     letter-spacing: 0.15em;
#     text-transform: uppercase;
#     color: #3a6070;
#     margin-bottom: 10px;
#   }
#   .big-num {
#     font-size: 36px;
#     line-height: 1;
#   }
#   .big-num.cyan   { color: #00c8e0; }
#   .big-num.green  { color: #00e5aa; }
#   .big-num.amber  { color: #e5b800; }
#   .big-num.pink   { color: #e06090; }
#   .big-num.purple { color: #c084fc; }
#   .big-num.orange { color: #fb923c; }
#   .sub { font-size: 11px; color: #3a6070; margin-top: 6px; }

#   /* table */
#   table { width: 100%; border-collapse: collapse; }
#   thead th {
#     font-size: 10px; letter-spacing: 0.12em; text-transform: uppercase;
#     color: #3a6070; padding: 8px 12px; text-align: left;
#     border-bottom: 1px solid #1a2a36;
#   }
#   tbody tr { border-bottom: 1px solid #111a22; transition: background 0.15s; }
#   tbody tr:hover { background: #0a1f28; }
#   tbody tr.new-row { animation: rowflash 0.5s ease; }
#   @keyframes rowflash { from { background: #0a2a20; } to { background: transparent; } }
#   tbody td { font-size: 13px; padding: 9px 12px; }
#   td.ts    { color: #3a6070; font-size: 11px; }
#   td.x-val { color: #00e5aa; }
#   td.y-val { color: #e5b800; }
#   td.th-val { color: #e06090; }
#   td.ts-val { color: #00c8e0; }
#   td.sp-val { color: #c084fc; }
#   td.rd-val { color: #fb923c; }

#   /* command */
#   .cmd-row { display: flex; gap: 10px; align-items: center; flex-wrap: wrap; }
#   .cmd-label { font-size: 12px; color: #3a6070; white-space: nowrap; }
#   input[type=number] {
#     width: 130px;
#     background: #0a0f14; border: 1px solid #1a2a36;
#     border-radius: 3px; color: #00c8e0;
#     font-family: inherit; font-size: 15px;
#     padding: 8px 10px; outline: none;
#   }
#   input[type=number]:focus { border-color: #00c8e0; }
#   button {
#     font-family: inherit; font-size: 11px; letter-spacing: 0.1em;
#     text-transform: uppercase; padding: 8px 16px;
#     background: transparent; border: 1px solid #00c8e0;
#     color: #00c8e0; border-radius: 3px; cursor: pointer;
#     white-space: nowrap; transition: background 0.15s, color 0.15s;
#   }
#   button:hover { background: #00c8e0; color: #0a0f14; }
#   button.enc-btn { border-color: #3a6070; color: #3a6070; }
#   button.enc-btn.on { border-color: #00e5aa; color: #00e5aa; }
#   button.enc-btn:hover { background: #00e5aa; color: #0a0f14; border-color: #00e5aa; }
#   #feedback { font-size: 11px; color: #00e5aa; margin-top: 10px; min-height: 16px; opacity: 0; transition: opacity 0.3s; }
#   #feedback.show { opacity: 1; }
# </style>
# </head>
# <body>
# <div class="panel">
#   <h1>
#     ESP//32 Monitor
#     <span id="enc-badge">ENCRYPT: OFF</span>
#   </h1>

#   <!-- stat cards -->
#   <div class="stats-row">
#     <div class="block">
#       <div class="block-label">Packets</div>
#       <div class="big-num cyan" id="stat-count">0</div>
#     </div>
#     <div class="block">
#       <div class="block-label">Latest X</div>
#       <div class="big-num green" id="stat-x">—</div>
#       <div class="sub">metres</div>
#     </div>
#     <div class="block">
#       <div class="block-label">Latest Y</div>
#       <div class="big-num amber" id="stat-y">—</div>
#       <div class="sub">metres</div>
#     </div>
#     <div class="block">
#       <div class="block-label">Latest Theta</div>
#       <div class="big-num pink" id="stat-theta">—</div>
#       <div class="sub">radians</div>
#     </div>
#     <div class="block">
#       <div class="block-label">Latest Speed</div>
#       <div class="big-num purple" id="stat-speed">—</div>
#       <div class="sub">m/s</div>
#     </div>
#     <div class="block">
#       <div class="block-label">Latest Rudder</div>
#       <div class="big-num orange" id="stat-rudder">—</div>
#       <div class="sub">degrees</div>
#     </div>
#   </div>

#   <!-- packet table -->
#   <div class="block" style="padding:0;">
#     <div style="padding:16px 20px 10px; font-size:10px; letter-spacing:0.15em; text-transform:uppercase; color:#3a6070;">
#       Last 10 packets
#     </div>
#     <table>
#       <thead>
#         <tr>
#           <th>Time</th>
#           <th>X (m)</th>
#           <th>Y (m)</th>
#           <th>Theta (rad)</th>
#           <th>Speed (m/s)</th>
#           <th>Rudder (°)</th>
#           <th>Uptime (s)</th>
#         </tr>
#       </thead>
#       <tbody id="log-body"></tbody>
#     </table>
#   </div>

#   <!-- command panel -->
#   <div class="block">
#     <div class="block-label">Commands</div>
#     <div class="cmd-row">
#       <button class="enc-btn" id="enc-btn" onclick="toggleEncryption()">Encryption: OFF</button>
#     </div>
#     <div id="feedback">&#10003; queued</div>
#   </div>
# </div>

# <script>
# var lastSeq = -1;
# var encOn   = false;

# function poll() {
#   fetch('/api/data?t=' + Date.now())
#     .then(function(r) { return r.json(); })
#     .then(function(d) {
#       if (!d.points || d.points.length === 0) return;
#       var latest = d.points[d.points.length - 1];
#       if (latest.seq === lastSeq) return;
#       lastSeq = latest.seq;

#       // stat cards
#       document.getElementById('stat-count').textContent  = d.total_count;
#       document.getElementById('stat-x').textContent      = parseFloat(latest.x).toFixed(3);
#       document.getElementById('stat-y').textContent      = parseFloat(latest.y     || 0).toFixed(3);
#       document.getElementById('stat-theta').textContent  = parseFloat(latest.theta || 0).toFixed(4);
#       document.getElementById('stat-speed').textContent  = parseFloat(latest.speed  || 0).toFixed(3);
#       document.getElementById('stat-rudder').textContent = parseFloat(latest.rudder || 0).toFixed(2);

#       // encryption badge
#       var badge = document.getElementById('enc-badge');
#       var encBtn = document.getElementById('enc-btn');
#       if (d.encryption_status) {
#         badge.textContent = 'ENCRYPT: ON';
#         badge.classList.add('on');
#       } else {
#         badge.textContent = 'ENCRYPT: OFF';
#         badge.classList.remove('on');
#       }

#       // table — last 10 newest first
#       var last10 = d.points.slice(-10).reverse();
#       var tbody  = document.getElementById('log-body');
#       tbody.innerHTML = '';
#       last10.forEach(function(p, i) {
#         var tr = document.createElement('tr');
#         if (i === 0) tr.className = 'new-row';
#         tr.innerHTML =
#           '<td class="ts">'    + p.received_at.slice(11,19)              + '</td>' +
#           '<td class="x-val">' + parseFloat(p.x).toFixed(4)             + '</td>' +
#           '<td class="y-val">' + parseFloat(p.y      || 0).toFixed(4)   + '</td>' +
#           '<td class="th-val">'+ parseFloat(p.theta  || 0).toFixed(5)   + '</td>' +
#           '<td class="sp-val">'+ parseFloat(p.speed  || 0).toFixed(3)   + '</td>' +
#           '<td class="rd-val">'+ parseFloat(p.rudder || 0).toFixed(2)   + '</td>' +
#           '<td class="ts-val">'+ p.timestamp                             + '</td>';
#         tbody.appendChild(tr);
#       });
#     })
#     .catch(function(e) { console.warn('poll error', e); });
# }

# function showFeedback(msg) {
#   var fb = document.getElementById('feedback');
#   fb.textContent = msg;
#   fb.classList.add('show');
#   setTimeout(function() { fb.classList.remove('show'); }, 3000);
# }

# function toggleEncryption() {
#   encOn = !encOn;
#   fetch('/set_encryption', {
#     method: 'POST',
#     headers: { 'Content-Type': 'application/json' },
#     body: JSON.stringify({ encryption_status: encOn })
#   }).then(function() {
#     var btn = document.getElementById('enc-btn');
#     btn.textContent = encOn ? 'Encryption: ON' : 'Encryption: OFF';
#     btn.classList.toggle('on', encOn);
#     showFeedback('\\u2713 encryption_status set to ' + (encOn ? 'TRUE' : 'FALSE'));
#   });
# }

# poll();
# setInterval(poll, 2000);
# </script>
# </body>
# </html>"""


# # ─── ROUTES ────────────────────────────────────────────────────────────────

# @app.route("/")
# def dashboard():
#     return Response(DASHBOARD_HTML, mimetype="text/html")


# @app.route("/data", methods=["POST"])
# def receive_data():
#     global pending_set_x, total_received, encryption_status

#     if not request.is_json:
#         return jsonify({"error": "Expected JSON"}), 400

#     packet = request.get_json()
#     if "timestamp" not in packet or "x" not in packet:
#         return jsonify({"error": "Missing fields"}), 422

#     total_received += 1
#     entry = {
#         "seq":         total_received,
#         "timestamp":   packet["timestamp"],
#         "x":           packet["x"],
#         "y":           packet.get("y",      0.0),
#         "theta":       packet.get("theta",  0.0),
#         "speed":       packet.get("speed",  0.0),
#         "rudder":      packet.get("rudder", 0.0),
#         "received_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     }
#     data_log.append(entry)

#     now = datetime.now().strftime("%H:%M:%S")
#     print(
#         f"[{now}]  seq={total_received}"
#         f"  ts={entry['timestamp']}s"
#         f"  x={entry['x']:.3f}"
#         f"  y={entry['y']:.3f}"
#         f"  theta={entry['theta']:.4f} rad"
#         f"  speed={entry['speed']:.3f} m/s"
#         f"  rudder={entry['rudder']:.2f} deg"
#         f"  ENCRYPT_STATUS={'TRUE' if encryption_status else 'FALSE'}"
#     )

#     response = {
#         "status":            "ok",
#         "encryption_status": encryption_status
#     }
#     if pending_set_x is not None:
#         response["set_x"] = pending_set_x
#         print(f"  --> Sending command: set_x = {pending_set_x}")
#         pending_set_x = None

#     return jsonify(response), 200


# @app.route("/set_encryption", methods=["POST"])
# def set_encryption():
#     """Manually flip encryption_status from the dashboard or curl.
#     Body: {"encryption_status": true} or {"encryption_status": false}
#     """
#     global encryption_status
#     if not request.is_json:
#         return jsonify({"error": "Expected JSON"}), 400
#     body = request.get_json()
#     if "encryption_status" not in body:
#         return jsonify({"error": "Missing encryption_status field"}), 422
#     encryption_status = bool(body["encryption_status"])
#     print(f"  --> encryption_status set to {'TRUE' if encryption_status else 'FALSE'}")
#     return jsonify({"encryption_status": encryption_status}), 200


# @app.route("/api/data", methods=["GET"])
# def api_data():
#     resp = jsonify({
#         "points":            list(data_log),
#         "total_count":       total_received,
#         "encryption_status": encryption_status
#     })
#     resp.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"
#     resp.headers["Pragma"]        = "no-cache"
#     resp.headers["Expires"]       = "0"
#     return resp, 200


# @app.route("/command", methods=["POST"])
# def send_command():
#     global pending_set_x
#     if not request.is_json:
#         return jsonify({"error": "Expected JSON"}), 400
#     cmd = request.get_json()
#     if "set_x" in cmd:
#         pending_set_x = float(cmd["set_x"])
#         return jsonify({"queued": True, "set_x": pending_set_x}), 200
#     return jsonify({"error": "Unknown command"}), 400


# @app.route("/status", methods=["GET"])
# def status():
#     return jsonify({"server": "running", "pending_set_x": pending_set_x}), 200


# # ─── ENTRY POINT ───────────────────────────────────────────────────────────
# if __name__ == "__main__":
#     print("ESP32 host server starting on http://0.0.0.0:5000")
#     print("  GET  /                 <- dashboard")
#     print("  POST /data             <- ESP32 posts here")
#     print("  GET  /api/data         <- browser polls here")
#     print("  POST /command          <- send set_x command")
#     print("  POST /set_encryption   <- set encryption_status true/false")
#     app.run(host="0.0.0.0", port=5000, debug=True)

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