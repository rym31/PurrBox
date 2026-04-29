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
 








 


 



