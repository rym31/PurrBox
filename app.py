from flask import Flask, jsonify, request
from flask_cors import CORS
import pigpio

# CONSTANTES
# RGB 1
R1 = 27
G1 = 22
B1 = 17
# RGB 2
R2 = 5
G2 = 16
B2 = 25
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
# RGB 1
pi.set_mode(R1,pigpio.OUTPUT)
pi.set_mode(G1,pigpio.OUTPUT)
pi.set_mode(B1,pigpio.OUTPUT)
# RGB 2
pi.set_mode(R2,pigpio.OUTPUT)
pi.set_mode(G2,pigpio.OUTPUT)
pi.set_mode(B2,pigpio.OUTPUT)
# Moteur
pi.set_mode(M1,pigpio.OUTPUT)
pi.set_mode(M2,pigpio.OUTPUT)
pi.set_mode(M3,pigpio.OUTPUT)
pi.set_mode(M4,pigpio.OUTPUT)
# Initialisation des RGB éteintes
# RGB 1
pi.write(R1, 1)
pi.write(G1, 1)
pi.write(B1, 1)
# RGB 2
pi.write(R2, 1)
pi.write(G2, 1)
pi.write(B2, 1)

# FONCTIONS
def set_max_limitation():
    pass

def set_rgbs(r1,g1,b1,r2,g2,b2):
    # set_PWM_dutycycle()
    pi.write(R1, r1)
    pi.write(G1, g1)
    pi.write(B1, b1)
    pi.write(R2, r2)
    pi.write(G2, g2)
    pi.write(B2, b2)



# ROUTES
@app.route('/',methods=['GET'])
def bonjour():
    return "<h1>Bonjour le monde!</h1>"


@app.route('/',methods=['POST'])
def bonjour():
    return "<h1>Bonjour le monde!</h1>"



# MAIN
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=3000)