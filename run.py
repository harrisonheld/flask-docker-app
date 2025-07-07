from flask import Flask, render_template, request, redirect, url_for
import subprocess
import socket

app = Flask(__name__)

servers = {}  # port -> subprocess.Popen
available_ports = list(range(10666, 10671))  # example port range

IWAD = 'DOOM2.WAD'
PWAD = 'back-to-saturn-x.pk3'

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

def get_server_command(port):
    return [
        'zandronum-server',
        '-host',
        '-port', str(port),
        '-iwad', IWAD,
        '-file', PWAD,
        '+sv_hostname', f"Doom Server {port}",
        '+deathmatch', '1'
    ]

def get_join_command(ip, port):
    return f"zandronum -iwad {IWAD} -file {PWAD} -connect {ip}:{port}"

def start_doom_server(port):
    if port in servers and servers[port].poll() is None:
        return False, "Server already running on this port."

    server_cmd = get_server_command(port)
    print(f"Starting server with command: {' '.join(server_cmd)}", flush=True)

    try:
        proc = subprocess.Popen(server_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        servers[port] = proc
        return True, f"Server started on port {port}"
    except Exception as e:
        return False, f"Failed to start server: {e}"

def stop_doom_server(port):
    if port in servers:
        proc = servers[port]
        proc.terminate()
        proc.wait(timeout=5)
        del servers[port]
        return True, f"Server on port {port} stopped."
    return False, f"No server running on port {port}."

@app.route("/", methods=["GET", "POST"])
def index():
    message = None
    error = None
    local_ip = get_local_ip()

    if request.method == "POST":
        action = request.form.get("action")
        port = int(request.form.get("port", 0))
        if action == "start":
            success, msg = start_doom_server(port)
        elif action == "stop":
            success, msg = stop_doom_server(port)
        else:
            success, msg = False, "Unknown action"
        if success:
            message = msg
        else:
            error = msg
        return redirect(url_for("index"))

    running_ports = [p for p in servers if servers[p].poll() is None]
    join_commands = {port: get_join_command(local_ip, port) for port in running_ports}

    return render_template(
        "index.html",
        running_ports=running_ports,
        available_ports=available_ports,
        local_ip=local_ip,
        join_commands=join_commands,
        message=message,
        error=error,
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
