import pigpio
import time

# GPIO
M1,M2,M3,M4 = 26,13,19,6

# Minimum recommandé: 2ms (0.002)
step_pause = 0.002

# Séquence "Single coil" 
seq_simple = [
    [1,0,0,0],
    [0,1,0,0],
    [0,0,1,0],
    [0,0,0,1]
]

# Séquence "Full-step" = plus de couple 
seq_full = [
    [1,0,0,1],
    [1,1,0,0],
    [0,1,1,0],
    [0,0,1,1]
]

# Séquence "Half-step" = plus de précision
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

def stop_moteur():
    pi.write(M1, 0)
    pi.write(M2, 0)
    pi.write(M3, 0)
    pi.write(M4, 0)

pi = pigpio.pi()

pi.set_mode(M1,pigpio.OUTPUT)
pi.set_mode(M2,pigpio.OUTPUT)
pi.set_mode(M3,pigpio.OUTPUT)
pi.set_mode(M4,pigpio.OUTPUT)

try:
    while True:
        for step in seq_simple: # Changez la séquence ici au besoin
            # Activer chacune des 4 bobines
            pi.write(M1, step[0])
            pi.write(M2, step[1])
            pi.write(M3, step[2])
            pi.write(M4, step[3])

            # La durée de la pause détermine la vitesse
            time.sleep(step_pause)

except KeyboardInterrupt:
    stop_moteur()