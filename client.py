import pigpio
import time
import socket

PORT = 5000
# DEST_IP = "192.168.13.1"
DEST_IP = "127.0.0.1"
MESSAGE = "abcdefg!\n"


# CONSTANTES
# RGB 
R = 27
G = 22
B = 17

# Moteur
STEPS_PAR_TOUR = 2048
M1,M2,M3,M4 = 26,13,19,6
step_pause = 0.002
# Séquence "Half-step" = plus de précision

# Distance
TRIG = 23
ECHO = 24


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

seq_half = [
    [1,0,0,0],
    [1,1,0,0],
    [0,1,0,0],
    [0,1,1,0],
    [0,0,1,0],
    [0,0,1,1],
    [0,0,0,1],
    [1,0,0,1]
]

# FONCTIONS
def degree_to_steps(angle):
    return angle / 360 * 2048

def stop_moteur():
    pi.write(M1, 0)
    pi.write(M2, 0)
    pi.write(M3, 0)
    pi.write(M4, 0)

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


def actionner_moteur(nb_portions):
    for i in range(int(nb_portions)):
        for step in seq_half:
            pi.write(M1, step[0])
            pi.write(M2, step[1])
            pi.write(M3, step[2])
            pi.write(M4, step[3])
            time.sleep(step_pause)
    stop_moteur()

def faire_clignoter_rgb():
    pass

# MAIN
if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((DEST_IP, PORT))
    try:
        while True:
            dist = lecture_distance()
            if dist <= 100:
                print(f"dist:{dist} cm")
                sock.send(f"{dist}\n".encode())
            else:
                print("Trop loin")
            time.sleep(0.5)
    except KeyboardInterrupt:
        pass
    finally:
        sock.close()
