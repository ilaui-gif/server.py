from flask import Flask, jsonify, request
from flask_socketio import SocketIO
import socket
from datetime import datetime

app = Flask(__name__)
# Erlaubt die Kommunikation zwischen den Skripten
socketio = SocketIO(app, cors_allowed_origins="*")

def get_server_local_ip():
    # Dein alter Code: Ermittelt die IP des Rechners im Netzwerk
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

@app.route("/api/getip")
def get_ip():
    # 1. IP des Besuchers (Anrufer-ID)
    # Prüft auch auf VPN/Proxy-Weiterleitungen
    visitor_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    if visitor_ip and ',' in visitor_ip:
        visitor_ip = visitor_ip.split(',')[0]

    # 2. Die IP dieses Servers (dein alter Wunschwert)
    server_ip = get_server_local_ip()
    
    # Zeitstempel für das Protokoll
    now = datetime.now().strftime("%H:%M:%S")

    # DATEN AN TERMINAL SENDEN
    socketio.emit('update_terminal', {
        'visitor': visitor_ip,
        'server': server_ip,
        'time': now
    })

    return jsonify({
        "status": "Erfolgreich",
        "ihre_ip_erkannt": visitor_ip,
        "server_lokal_ip": server_ip
    })

import os

if __name__ == "__main__":
    # Render weist uns einen Port über die Umgebungsvariable zu
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host="0.0.0.0", port=port)