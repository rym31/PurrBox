# from flask import Flask, jsonify, request, render_template
# from flask_cors import CORS
# import socket
# import threading
 
# # INITIALISATIONS
# # TCP
# PORT = 5008
# BUFFER_SIZE = 1024
 
# # Flask
# app = Flask(__name__)
# CORS(app)
 
# socket_local = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# address = ('', PORT)  
 
# # Lier le socket à l'adresse
# socket_local.bind(address)
 
# # Attendre une connexion
# socket_local.listen(3)
# print(f"Serveur TCP en écoute au port {PORT}...")
 
# socket_dist, client_address = socket_local.accept()
# print(f"Socket distant: {client_address}")

# # État partagé
# etat = {
#     "derniere_distance": None,
#     "dernier_message": None,
#     "nb_distributions": 0,
#     "nb_tentatives": 0,
#     "actif": False,
# }

# # FONCTIONS
# def creer_socket():
#     buffer = ""
#     presence_chat = False
#     while True:
#         data = socket_dist.recv(BUFFER_SIZE)
#         if not data:
#             print("Déconnecté")
#             break
#         buffer += data.decode()
#         while "\n" in buffer:
#             ligne, buffer = buffer.split("\n", 1)
#             ligne = ligne.strip()
#             if ligne:
#                 if ligne == "POWER_ON":
#                     etat["actif"] = True
#                     print("Système activé")
#                 elif ligne == "POWER_OFF":
#                     etat["actif"] = False
#                     print("Système désactivé")
#                 else:
#                     dist = float(ligne)
#                     etat["derniere_distance"] = dist
#                     etat["dernier_message"] = ligne
#                     print(f"Reçu: {dist} cm")
                    
#                     if dist <= 15:
#                         if not presence_chat:
#                             presence_chat = True
#                             etat["nb_tentatives"] +=1
#                             print("Chat!")
#                     else:
#                         presence_chat = False
                         
# # ROUTES
# @app.route('/')
# def home():
#     return render_template('index2.html')

# @app.route('/api/status', methods=['GET'])
# def api_status():
#     return jsonify(etat)

# @app.route('/api/power', methods=['POST'])
# def api_power():
#     json_data = request.get_json()
#     if not json_data or "etat" not in json_data:
#         return jsonify({'Erreur': 'Mauvais attribut'}), 400
#     if json_data["etat"] == "on":
#         etat["actif"] = True
#     elif json_data["etat"] == "off":
#         etat["actif"] = False
#     else:
#         return jsonify({'Erreur': 'Mauvaise valeur'}), 400
#     return jsonify({'actif': etat["actif"]}), 200

# @app.route('/api/rgb', methods=['POST'])
# def api_rgb():
#     json_data = request.get_json()
#     if not json_data or "etat" not in json_data:
#         return jsonify({'Erreur': 'Mauvais attribut'}), 400
#     if json_data["etat"] in ("on", "off"):
#         etat["actif"] = json_data["etat"] == "on"
#     else:
#         return jsonify({'Erreur': 'Mauvaise valeur'}), 400
#     return jsonify({'actif': etat["actif"]}), 200

# @app.route('/api/feed', methods=['POST'])
# def api_feed():
#     json_data = request.get_json()
#     portions = int(json_data.get("portions", 1)) if json_data else 1
#     socket_dist.send(f"FEED:{portions}\n".encode())
#     etat["nb_distributions"] += portions
#     return jsonify({"portions": portions}), 200


# # INITIALISATION DES THREADS
# # thread_logique_materielle = threading.Thread(target=logique_materielle, daemon=True)
# thread_creer_socket = threading.Thread(target=creer_socket, daemon=True)
# # MAIN
# if __name__ == '__main__':
 
#     try:
#     #     thread_logique_materielle.start()
#         thread_creer_socket.start()  
#         app.run(host='0.0.0.0',port=5000)
#     #     thread_logique_materielle.join()
#         thread_creer_socket.join()
#     except KeyboardInterrupt:
#         socket_dist.close()
#         socket_local.close() 

from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import socket
import threading

PORT_TCP = 5008
PORT_FLASK = 5000
BUFFER_SIZE = 1024

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
    return jsonify({"portions": portions}), 200

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