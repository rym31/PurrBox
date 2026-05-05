from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import socket
import threading
 
# INITIALISATIONS
# TCP
PORT = 5000
BUFFER_SIZE = 1024
 
# Flask
app = Flask(__name__)
CORS(app)
 
socket_local = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
address = ('', PORT)  
 
# Lier le socket à l'adresse
socket_local.bind(address)
 
# Attendre une connexion
socket_local.listen(3)
print(f"Serveur TCP en écoute au port {PORT}...")
 
socket_dist, client_address = socket_local.accept()
print(f"Socket distant: {client_address}")

# État partagé
etat = {
    "derniere_distance": None,
    "dernier_message": None,
    "nb_distributions": 0,
    "nb_tentatives": 0,
}

# FONCTIONS
def creer_socket():
    buffer = ""
    while True:
        data = socket_dist.recv(BUFFER_SIZE)
        if not data:
            print("Déconnecté")
            break
        buffer += data.decode()
        while "\n" in buffer:
            ligne, buffer = buffer.split("\n", 1)
            ligne = ligne.strip()
            if ligne:
                print(f"Reçu: {ligne} cm")
                etat["derniere_distance"] = float(ligne)
                etat["dernier_message"] = ligne
 
# ROUTES
@app.route('/')
def home():
    return render_template('index2.html')

@app.route('/api/status', methods=['GET'])
def api_status():
    return jsonify(etat)
 
@app.route('/rgb', methods=['POST'])
def set_rgb():
    if request.method == "POST":
        json_data = request.get_json()
        if "etat" in json_data:
            if json_data["etat"] == "on":
                pass
                # pi.write(R, 1)
                # pi.write(G, 0)
                # pi.write(B, 1)
               
                # va être envoyé par le client
                # lecture_distance()
            elif json_data["etat"] == "off":
                pass
                # pi.write(R, 0)
                # pi.write(G, 1)
                # pi.write(B, 1)
            else:
                return jsonify({'Erreur': 'Mauvaise valeur'}), 500
        else:
            return jsonify({'Erreur': 'Mauvais attribut'}), 500
    else:
        return jsonify({'Erreur': 'Requetes POST seulement'}), 500
 
    return jsonify({'Succes': 'ok'}), 200
 
 
# INITIALISATION DES THREADS
# thread_logique_materielle = threading.Thread(target=logique_materielle, daemon=True)
thread_creer_socket = threading.Thread(target=creer_socket, daemon=True)
# MAIN
if __name__ == '__main__':
 
    try:
    #     thread_logique_materielle.start()
        thread_creer_socket.start()  
        app.run(host='0.0.0.0',port=5001)
    #     thread_logique_materielle.join()
        thread_creer_socket.join()
    except KeyboardInterrupt:
        socket_dist.close()
        socket_local.close()
 