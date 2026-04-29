# import pigpio
# import time
# from time import sleep

# # Proxemity detection ultrasonic
# TRIG = 25 
# ECHO = 24 
# SOUNDSPEED = 343 # Vitesse du son 343 m/s



# # INITIALISATIONS
# # pi
# pi = pigpio.pi()


# # Proxemity detection ultrasonic
# pi.set_mode(TRIG,pigpio.OUTPUT) # Branche de sorties
# pi.set_mode(ECHO,pigpio.INPUT) # Branche d'entrées
# pi.write(TRIG,0)


# lastClick = 1
# timer = 0
# confirmDuration = False
# done = False

# oppened = False

# # Si échec de la connection avec le pi
# if not pi.connected:
#     print("Impossible de se connecter à pigpio.")
#     exit()
# try:
#     while True:

#         # Envoyer l'ultrason
#         pi.write(TRIG,1)
#         time.sleep(0.00001) # Pulse de 10 µ (microsecondes)
#         pi.write(TRIG,0)

#         # Attendre l'echo
#         while pi.read(ECHO) == 0: 
#             signalStart = time.time()

#         # Attendre la fin de l'echo
#         while pi.read(ECHO) == 1: 
#             endSignal = time.time()

#         # Calculer le distance
#         # On divise par 2 car le son fait 2x la distance (aller-retour)
#         durationSignal = endSignal - signalStart
#         distance = durationSignal * SOUNDSPEED / 2 
#         distance = round(distance,1)

#         print(ECHO)


        
# except KeyboardInterrupt:
#     pi.stop()
#     print(" Programme terminé par l'utilisateur à l'aide des touches du clavier.")




from datetime import datetime
import pigpio
import time
 
 
pi = pigpio.pi()
 
TRIG = 23
ECHO = 24
R = 27
G = 22
B = 17


pi.set_mode(TRIG, pigpio.OUTPUT)
pi.set_mode(ECHO, pigpio.INPUT)
pi.set_mode(R,pigpio.OUTPUT)
pi.set_mode(G,pigpio.OUTPUT)
pi.set_mode(B,pigpio.OUTPUT)
  
pi.write(R, 1)
pi.write(G, 1)
pi.write(B, 1)
 
dist = 0


 
def set_led(r, g, b):
    pi.write(R, r)
    pi.write(G, g)
    pi.write(B, b)
 
def lecture_distance():
    # Déclenchement (Impulsion de 10µs)
    pi.write(TRIG, 1)
    time.sleep(0.00001)
    pi.write(TRIG, 0)
 
    start = time.time()
    stop = time.time()
 
    # Attente du début de l'écho
    while pi.read(ECHO) == 0:
        start = time.time()
    
    # Attente de la fin de l'écho
    while pi.read(ECHO) == 1:
        stop = time.time()
 
    duree = stop - start
    return round((duree * 34300) / 2, 1)

try:
    while True:
        dist = lecture_distance()
        if dist <= 100:
            print(f"dist:{dist}")
        else :
            print("Trop Loin")
        
        time.sleep(0.1)

except KeyboardInterrupt:
    set_led(1, 1, 1)
 




# from flask import Flask, jsonify, request
# import socket
# from datetime import datetime
# import pigpio
# from flask_cors import CORS
# import time
# import threading
 
 
 
# threshold = 50
# app = Flask(__name__)
# CORS(app)
# pi = pigpio.pi()
 
# TRIG = 15
# ECHO = 14
# R = 19
# G = 26
# B = 13
 
# dist = 0
 
# pi.set_mode(R,pigpio.OUTPUT)
# pi.set_mode(G,pigpio.OUTPUT)
# pi.set_mode(B,pigpio.OUTPUT)
  
# pi.write(R, 1)
# pi.write(G, 1)
# pi.write(B, 1)
 

# @app.route('/',methods=['GET'])
# def bonjour():
#     return "<h1>Bonjour le monde!</h1>"
# @app.route('/get_distance',methods=['GET'])
# def distance():
#     return jsonify({'distance': dist})
# @app.route('/set_threshold', methods=['POST'])
# def set_threshold():
#     global threshold
#     if request.method == "POST":
#       json = request.get_json()
#       print(json)
#       if "threshold" in json:
#         threshold = json['threshold']
#       else:
#           return jsonify({'Erreur': 'Mauvais attribut'}),500
#     else:
#         return jsonify({'Erreur': 'Requetes POST seulement'}),500
#     return jsonify({'Etat': json}),200
   
 
# def set_led(r, g, b):
#     pi.write(R, r)
#     pi.write(G, g)
#     pi.write(B, b)
 
# def update_led(dist):
#     global threshold
#     if dist < threshold / 2:
#         set_led(0, 1, 1)
#     elif dist <= threshold:
#         set_led(0, 0, 1)
#     else:
#         set_led(1, 0, 1)
# def lecture_distance():
#     # Déclenchement (Impulsion de 10µs)
#     pi.write(TRIG, 1)
#     time.sleep(0.00001)
#     pi.write(TRIG, 0)
 
#     start = time.time()
#     stop = time.time()
 
#     # Attente du début de l'écho
#     while pi.read(ECHO) == 0:
#         start = time.time()
    
#     # Attente de la fin de l'écho
#     while pi.read(ECHO) == 1:
#         stop = time.time()
 
#     duree = stop - start
#     return round((duree * 34300) / 2, 1)
 
# def logique_pi():
#   global threshold
#   global dist
#   try:
#       while True:
#           print(f"threshold:{threshold}")
#           dist = lecture_distance()
#           print(f"dist:{dist}")
#           update_led(dist)
#           time.sleep(1)
#   except KeyboardInterrupt:
#       set_led(1, 1, 1)
# thread_led1 = threading.Thread(target=logique_pi, daemon=True)
# thread_led1.start()
# app.run(host='0.0.0.0',port=5000)
# thread_led1.join()

#-------------------------------------------------------------------------------------------------------------------------

#Exercice 1
# #

# pi.set_mode(R,pigpio.OUTPUT)
# pi.set_mode(G,pigpio.OUTPUT)
# pi.set_mode(B,pigpio.OUTPUT)
  
# pi.write(R, 1)
# pi.write(G, 1)
# pi.write(B, 1)

# app = Flask(__name__)
# CORS(app)


# @app.route('/rgb', methods=['POST'])
# def set_led():
#     if request.method == "POST":
#       json = request.get_json()
#       if "etat" in json:
#         if json["etat"] == 0:
#             pi.write(R, 0)
#             pi.write(G, 1)
#             pi.write(B, 1)
#         elif json["etat"] == 1:
#             pi.write(R, 1)
#             pi.write(G, 0)
#             pi.write(B, 1)
#         elif json["etat"] == 2:
#             pi.write(R, 1)
#             pi.write(G, 1)
#             pi.write(B, 0)
#         else:
#             return jsonify({'Erreur': 'Mauvaise valeur'}),500
#       else:
#         return jsonify({'Erreur': 'Mauvais attribut'}),500
#     else:
#       return jsonify({'Erreur': 'Requetes POST seulement'}),500
#     return jsonify({'Etat': json["etat"]}),200
   
# if __name__ == '__main__':
#     app.run(host='0.0.0.0',port=5000)


 


 



