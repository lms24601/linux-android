#!/usr/bin/env python3
"""
Simple Flask web server to demo your Linux-on-Android setup.

Usage:
    pip install flask
    python hello_server.py

Then open Firefox and go to http://localhost:5000
"""

from flask import Flask
import platform
import os
import subprocess
import datetime

app = Flask(__name__)


def get_device_info():
    """Grab some system info to show off in the demo."""
    info = {}
    info["hostname"] = platform.node()
    info["arch"] = platform.machine()
    info["python"] = platform.python_version()

    # uptime
    try:
        with open("/proc/uptime") as f:
            secs = int(float(f.read().split()[0]))
            hrs, rem = divmod(secs, 3600)
            mins, secs = divmod(rem, 60)
            info["uptime"] = f"{hrs}h {mins}m {secs}s"
    except Exception:
        info["uptime"] = "N/A"

    # memory
    try:
        with open("/proc/meminfo") as f:
            for line in f:
                if line.startswith("MemTotal"):
                    kb = int(line.split()[1])
                    info["ram"] = f"{kb // 1024} MB"
                    break
    except Exception:
        info["ram"] = "N/A"

    # cpu
    try:
        cores = os.cpu_count() or "N/A"
        info["cpu_cores"] = str(cores)
    except Exception:
        info["cpu_cores"] = "N/A"

    return info


@app.route("/")
def home():
    info = get_device_info()
    now = datetime.datetime.now().strftime("%I:%M %p")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Linux on Android</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', system-ui, sans-serif;
            background: #0f0f0f;
            color: #e0e0e0;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        .container {{
            text-align: center;
            padding: 2rem;
            max-width: 600px;
        }}
        h1 {{
            font-size: 2.5rem;
            margin-bottom: 0.25rem;
            background: linear-gradient(135deg, #4fc3f7, #ab47bc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .subtitle {{
            color: #888;
            font-size: 1.1rem;
            margin-bottom: 2rem;
        }}
        .card {{
            background: #1a1a2e;
            border: 1px solid #333;
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            text-align: left;
        }}
        .card h2 {{
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 2px;
            color: #888;
            margin-bottom: 1rem;
        }}
        .stat-row {{
            display: flex;
            justify-content: space-between;
            padding: 0.4rem 0;
            border-bottom: 1px solid #262640;
        }}
        .stat-row:last-child {{ border-bottom: none; }}
        .stat-label {{ color: #aaa; }}
        .stat-value {{ color: #4fc3f7; font-weight: 600; }}
        .badge {{
            display: inline-block;
            background: #1b5e20;
            color: #69f0ae;
            padding: 0.3rem 0.75rem;
            border-radius: 20px;
            font-size: 0.85rem;
            margin-top: 1rem;
        }}
        .footer {{
            color: #555;
            font-size: 0.85rem;
            margin-top: 1rem;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Hello from Android!</h1>
        <p class="subtitle">A full Linux desktop running on a phone — no root, no PC.</p>

        <div class="card">
            <h2>System Info</h2>
            <div class="stat-row">
                <span class="stat-label">Architecture</span>
                <span class="stat-value">{info['arch']}</span>
            </div>
            <div class="stat-row">
                <span class="stat-label">Python</span>
                <span class="stat-value">{info['python']}</span>
            </div>
            <div class="stat-row">
                <span class="stat-label">CPU Cores</span>
                <span class="stat-value">{info['cpu_cores']}</span>
            </div>
            <div class="stat-row">
                <span class="stat-label">RAM</span>
                <span class="stat-value">{info['ram']}</span>
            </div>
            <div class="stat-row">
                <span class="stat-label">Uptime</span>
                <span class="stat-value">{info['uptime']}</span>
            </div>
        </div>

        <span class="badge">Flask server running at {now}</span>

        <p class="footer">Powered by Termux + Termux-X11</p>
    </div>
</body>
</html>"""


if __name__ == "__main__":
    print("\\n  Starting server at http://localhost:5000")
    print("  Open Firefox on your desktop and visit the URL above.\\n")
    app.run(host="0.0.0.0", port=5000)
