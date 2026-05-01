from flask import Flask, jsonify, request
from flask_cors import CORS
import pigpio

# CONSTANTES
# RGB 
R = 27
G = 22
B = 17
# Moteur
M1,M2,M3,M4 = 26,13,19,6
# Distance
TRIG = 23
ECHO = 24

# INITIALISATIONS
# Flask
app = Flask(__name__)
CORS(app)
# GPIO
pi = pigpio.pi()
# Set GPIO modes
# Distance
pi.set_mode(TRIG, pigpio.OUTPUT)
pi.set_mode(ECHO, pigpio.INPUT)
# RGB 
pi.set_mode(R,pigpio.OUTPUT)
pi.set_mode(G,pigpio.OUTPUT)
pi.set_mode(B,pigpio.OUTPUT)
# Moteur
pi.set_mode(M1,pigpio.OUTPUT)
pi.set_mode(M2,pigpio.OUTPUT)
pi.set_mode(M3,pigpio.OUTPUT)
pi.set_mode(M4,pigpio.OUTPUT)
# Initialisation des RGB éteintes
# RGB 
pi.write(R, 1)
pi.write(G, 1)
pi.write(B, 1)
# FONCTIONS
compteur = 0
def set_max_limitation():
    pass
    

def set_rgbs(r1,g1,b1,r2,g2,b2):
    # set_PWM_dutycycle()
    pi.write(R, r1)
    pi.write(G, g1)
    pi.write(B, b1)



# ROUTES
@app.route('/',methods=['GET'])
def bonjour():
    return "<h1>Bonjour le monde!</h1>"

@app.route('/rgb', methods=['POST'])
def set_rgb():
    if request.method == "POST":
        json_data = request.get_json()
        if "etat" in json_data:
            if json_data["etat"] == "on":
                pi.write(R, 1)
                pi.write(G, 0)
                pi.write(B, 1)
            elif json_data["etat"] == "off":
                pi.write(R, 0)
                pi.write(G, 1)
                pi.write(B, 1)
            else:
                return jsonify({'Erreur': 'Mauvaise valeur'}), 500
        else:
            return jsonify({'Erreur': 'Mauvais attribut'}), 500
    else:
        return jsonify({'Erreur': 'Requetes POST seulement'}), 500

    return jsonify({'Succes': 'ok'}), 200

# MAIN
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)
