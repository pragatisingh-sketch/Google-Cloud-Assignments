from flask import Flask, jsonify, render_template_string
import time
import os
from datetime import datetime, timezone, timedelta

app = Flask(__name__)
start_time = time.time()

cpu_history = [0.0] 
LOG_FILE = "history.log"


def get_india_time():
    """Calculates current time in IST (UTC+5:30)."""
    ist_delta = timedelta(hours=5, minutes=30)
    return datetime.now(timezone(ist_delta)).strftime("%Y-%m-%d %I:%M:%S %p")

def get_cpu_usage():
    """Safe calculation of CPU usage from /proc/stat."""
    def read_stat():
        try:
            with open("/proc/stat", "r") as f:
                fields = list(map(int, f.readline().split()[1:]))
            return fields[3], sum(fields)
        except: return 0, 0

    i1, t1 = read_stat()
    time.sleep(0.5)
    i2, t2 = read_stat()
    
    delta_t = t2 - t1
    # Ensure always returning a dict to avoid 'float' subscriptable error
    cpu = max(0.0, round(100 * (1 - (i2 - i1) / delta_t), 2)) if delta_t > 0 else 0.0
    cpu_history.append(cpu)
    return {"current": cpu, "highest": max(cpu_history), "lowest": min(cpu_history)}

def get_memory():
    """Safe calculation of Memory usage from /proc/meminfo."""
    try:
        mem = {}
        with open("/proc/meminfo") as f:
            for line in f:
                p = line.split(":")
                if len(p) == 2: mem[p[0]] = int(p[1].strip().split()[0])
        total = mem.get("MemTotal", 1)
        avail = mem.get("MemAvailable", mem.get("MemFree", total))
        return round((total - avail) / total * 100, 2)
    except: return 0.0

def calculate_health(cpu, mem):
    """Returns status based on resource usage."""
    score = 100 - ((cpu * 0.5) + (mem * 0.5))
    score = max(0, min(100, int(score)))
    if score > 70: return score, "Healthy System", "#10b981" 
    if score >= 40: return score, "Moderate Load", "#f59e0b"  
    return score, "Critical Load", "#ef4444"                

# ---------- ROUTES ----------

@app.route("/analyze")
def analyze():
    """This route explicitly returns JSON data."""
    cpu_data = get_cpu_usage()
    mem_val = get_memory()
    score, msg, color = calculate_health(cpu_data["current"], mem_val)

    # Prepare JSON response
    result = {
        "metrics": {
            "timestamp_ist": get_india_time(),
            "uptime": f"{int(time.time() - start_time)}s",
            "cpu_metric": cpu_data,
            "memory_usage": f"{mem_val}%",
            "health_score": score,
            "status": msg
        }
    }

    # Internal Logging
    try:
        with open(LOG_FILE, "a") as f:
            f.write(f"[{result['metrics']['timestamp_ist']}] Score: {score} | CPU: {cpu_data['current']}% | MEM: {mem_val}%\n")
        
        # Add updated logs to the same JSON response
        with open(LOG_FILE, "r") as f:
            result["logs"] = "".join(f.readlines()[-15:])
    except:
        result["logs"] = "Logging error or no history yet."

    return jsonify(result)

@app.route("/")
def home():
    cpu_data = get_cpu_usage()
    mem_val = get_memory()
    score, msg, color = calculate_health(cpu_data["current"], mem_val)
    
    logs_initial = "No system logs found."
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r") as f:
                logs_initial = "".join(f.readlines()[-15:])
        except: pass

    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Cloud Health Dashboard</title>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=JetBrains+Mono&display=swap" rel="stylesheet">
        <style>
            :root {{ --health-color: {color}; }}
            body {{ 
                margin: 0; padding: 0; font-family: 'Inter', sans-serif;
                background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
                color: #f8fafc; min-height: 100vh; display: flex; align-items: center; justify-content: center;
            }}
            .container {{ width: 95%; max-width: 1100px; padding: 20px; }}
            .card {{
                background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(12px);
                border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 16px; padding: 30px;
                box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
            }}
            .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 25px; margin-top: 25px; }}
            button {{
                width: 100%; background: #3b82f6; color: white; border: none; padding: 16px;
                border-radius: 12px; font-weight: 600; cursor: pointer; transition: 0.3s;
            }}
            button:hover {{ background: #2563eb; transform: translateY(-2px); }}
            pre {{ 
                background: #020617; color: #cbd5e1; padding: 15px; border-radius: 8px; 
                font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; 
                border: 1px solid #1e293b; height: 320px; overflow: auto; margin: 0;
            }}
            .label {{ color: #38bdf8; font-size: 0.7rem; text-transform: uppercase; margin-bottom: 8px; letter-spacing: 1px; }}
            #log-display {{ white-space: pre-wrap; word-break: break-all; color: #94a3b8; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div style="text-align:center; margin-bottom: 20px;">
                <h1 style="margin:0; font-weight:300;">Cloud Run <span style="color:var(--health-color)">Monitor</span></h1>
                <div style="background:var(--health-color); display:inline-block; padding:5px 15px; border-radius:20px; font-size:0.8rem; margin-top:10px;">{msg} — {score}%</div>
            </div>
            <div class="card">
                <button onclick="runAnalysis()" id="runBtn">Initiate System Analysis</button>
                <div class="grid">
                    <div>
                        <div class="label">JSON Result</div>
                        <pre id="json-display">System ready...</pre>
                    </div>
                    <div>
                        <div class="label">Recent History</div>
                        <pre id="log-display">{logs_initial}</pre>
                    </div>
                </div>
            </div>
        </div>
        <script>
            async function runAnalysis() {{
                const btn = document.getElementById('runBtn');
                const jsonBox = document.getElementById('json-display');
                const logBox = document.getElementById('log-display');
                btn.innerText = "Analyzing...";
                btn.disabled = true;

                try {{
                    const response = await fetch('/analyze');
                    const data = await response.json();
                    
                    // Display JSON metrics
                    jsonBox.innerText = JSON.stringify(data.metrics, null, 2);
                    // Update Logs from JSON response
                    logBox.innerText = data.logs;
                    logBox.scrollTop = logBox.scrollHeight;
                }} catch (e) {{
                    jsonBox.innerText = "Error: Route /analyze not responding.";
                }} finally {{
                    btn.innerText = "Initiate System Analysis";
                    btn.disabled = false;
                }}
            }}
        </script>
    </body>
    </html>
    """
    return render_template_string(html)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)





























