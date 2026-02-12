# from flask import Flask

# app = Flask(__name__)

# @app.route("/")
# def home():
#     return "Hello from Cloud Run! System check complete."

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=8080)




from flask import Flask, jsonify, render_template_string
import time
import os
from datetime import datetime

app = Flask(__name__)

# ---------------- CPU METRIC USING /proc/stat ----------------
def get_cpu_usage():
    def read_cpu():
        with open("/proc/stat", "r") as f:
            line = f.readline()
        values = [float(x) for x in line.strip().split()[1:]]
        idle = values[3]
        total = sum(values)
        return idle, total

    idle1, total1 = read_cpu()
    time.sleep(0.5)
    idle2, total2 = read_cpu()

    idle_delta = idle2 - idle1
    total_delta = total2 - total1

    cpu_usage = 100 * (1 - idle_delta / total_delta)
    return round(cpu_usage, 2)

# ---------------- MEMORY METRIC USING /proc/meminfo ----------------
def get_memory_usage():
    meminfo = {}
    with open("/proc/meminfo") as f:
        for line in f:
            key, value = line.split(":")
            meminfo[key] = int(value.strip().split()[0])

    total = meminfo["MemTotal"]
    available = meminfo["MemAvailable"]
    used = total - available
    usage_percent = (used / total) * 100

    return round(usage_percent, 2)

# ---------------- HEALTH SCORE LOGIC ----------------
def calculate_health(cpu, memory):
    score = 100

    if cpu > 80:
        score -= 30
    elif cpu > 60:
        score -= 15

    if memory > 80:
        score -= 30
    elif memory > 60:
        score -= 15

    if score < 0:
        score = 0

    return score

# ---------------- HOME PAGE WITH UI ----------------
@app.route("/")
def home():
    html = """
    <html>
    <head>
        <title>System Analyzer</title>
    </head>
    <body style="font-family: Arial; text-align:center; padding-top:50px;">
        <h1>Cloud Run System Analyzer</h1>
        <button onclick="check()" style="padding:15px 25px;font-size:18px;">
            Check System Health
        </button>

        <div id="result" style="margin-top:40px;font-size:22px;"></div>

        <script>
        async function check(){
            let res = await fetch('/analyze');
            let data = await res.json();

            let color = "white";

            if(data.health_score > 60){
                color = "lightgreen";
            }
            else if(data.health_score >= 40){
                color = "yellow";
            }
            else{
                color = "#ff7b7b";
            }

            document.body.style.background = color;

            document.getElementById("result").innerHTML =
            "Score: " + data.health_score + "<br>" +
            data.message + "<br><br>" +
            "CPU: " + data.cpu_metric + "%<br>" +
            "Memory: " + data.memory_metric + "%";
        }
        </script>
    </body>
    </html>
    """
    return render_template_string(html)

# ---------------- ANALYZE ENDPOINT ----------------
start_time = time.time()

@app.route("/analyze")
def analyze():
    cpu = get_cpu_usage()
    memory = get_memory_usage()

    uptime = int(time.time() - start_time)
    score = calculate_health(cpu, memory)

    if score > 60:
        msg = "Healthy system"
    elif score >= 40:
        msg = "Partially healthy"
    else:
        msg = "Not secure"

    return jsonify({
        "timestamp": datetime.utcnow().isoformat(),
        "uptime_seconds": uptime,
        "cpu_metric": cpu,
        "memory_metric": memory,
        "health_score": score,
        "message": msg
    })

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
