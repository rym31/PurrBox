import socket
 
PORT = 8888
BUFFER_SIZE = 1024
 
# Créer le socket
socket_local = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
address = ('', PORT)  
 
# Lier le socket à l'adresse
socket_local.bind(address)
 
# Attendre une connexion
socket_local.listen(3)
print(f"Serveur TCP en écoute au port {PORT}...")
 
socket_dist, client_address = socket_local.accept()
print(f"Socket distant: {client_address}")
 
# Réception des messages
while True:
    # Données
    data = socket_dist.recv(BUFFER_SIZE)
    if not data:
        print("Déconnecté")
        break
    else:
        # Décoder + afficher les message
        message = data.decode()
        print(f"Reçu: {message}", end='')
 
socket_dist.close()
socket_local.close()
 