from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import socket
import threading

PORT_TCP = 5008
PORT_FLASK = 5000
BUFFER_SIZE = 1024
MAX_DISTRIBUTIONS = 4

app = Flask(__name__, static_folder='static')
CORS(app)

socket_dist = None  # sera assigné après accept()

etat = {
    "derniere_distance": None,
    "dernier_message": None,
    "nb_distributions": 0,
    "nb_tentatives": 0,
    "actif": False,
}

def thread_tcp():
    global socket_dist

    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(('', PORT_TCP))
    srv.listen(3)
    print(f"TCP en écoute sur le port {PORT_TCP}...")

    while True:
        socket_dist, addr = srv.accept()  # bloque dans le thread, pas dans le main
        print(f"Pi connecté depuis {addr}")
        lire_messages()
        socket_dist = None
        print("Pi déconnecté, en attente...")

def lire_messages():
    buffer = ""
    presence_chat = False
    while True:
        try:
            data = socket_dist.recv(BUFFER_SIZE)
        except Exception as e:
            print(f"Erreur recv : {e}")
            break
        if not data:
            break
        buffer += data.decode()
        while "\n" in buffer:
            ligne, buffer = buffer.split("\n", 1)
            ligne = ligne.strip()
            if not ligne:
                continue
            if ligne == "POWER_ON":
                etat["actif"] = True
            elif ligne == "POWER_OFF":
                etat["actif"] = False
            else:
                try:
                    dist = float(ligne)
                    etat["derniere_distance"] = dist
                    etat["dernier_message"] = ligne
                    if dist <= 15:
                        if not presence_chat:
                            presence_chat = True
                            etat["nb_tentatives"] += 1
                    else:
                        presence_chat = False
                except ValueError:
                    print(f"Message inconnu : {ligne}")

@app.route('/')
def home():
    return render_template('index2.html')

@app.route('/api/status')
def api_status():
    return jsonify(etat)

@app.route('/api/feed', methods=['POST'])
def api_feed():
    if socket_dist is None:
        return jsonify({"erreur": "Pi non connecté"}), 503
    json_data = request.get_json()
    portions = int(json_data.get("portions", 1)) if json_data else 1
    socket_dist.send(f"FEED:{portions}\n".encode())
    etat["nb_distributions"] += portions
    if etat["nb_distributions"] > MAX_DISTRIBUTIONS:
        etat["reservoir_plein"] = False
    return jsonify({"portions": portions}), 200

@app.route('/api/reset_reservoir', methods=['POST'])
def api_reset_reservoir():
    etat["reservoir_plein"] = True
    return jsonify({"ok": True}), 200

@app.route('/api/power', methods=['POST'])
def api_power():
    json_data = request.get_json()
    if not json_data or "etat" not in json_data:
        return jsonify({'erreur': 'Mauvais attribut'}), 400
    etat["actif"] = json_data["etat"] == "on"
    return jsonify({'actif': etat["actif"]}), 200

if __name__ == '__main__':
    threading.Thread(target=thread_tcp, daemon=True).start()
    app.run(host='0.0.0.0', port=PORT_FLASK)
