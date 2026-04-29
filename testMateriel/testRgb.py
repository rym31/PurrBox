import pigpio
import time


R1 = 27
G1 = 22
B1 = 17

R2 = 5
G2 = 16
B2 = 25

pi = pigpio.pi()



pi.set_mode(R1,pigpio.OUTPUT)
pi.set_mode(G1,pigpio.OUTPUT)
pi.set_mode(B1,pigpio.OUTPUT)

pi.set_mode(R2,pigpio.OUTPUT)
pi.set_mode(G2,pigpio.OUTPUT)
pi.set_mode(B2,pigpio.OUTPUT)

try:
    while True:
        pi.write(R1, 0)
        pi.write(G1, 1)
        pi.write(B1, 1)

        time.sleep(0.5)

        pi.write(R1, 1)
        pi.write(G1, 0)
        pi.write(B1, 1)

        time.sleep(0.5)

        pi.write(R1, 1)
        pi.write(G1, 1)
        pi.write(B1, 0)

        time.sleep(0.5)

        pi.write(R2, 0)
        pi.write(G2, 1)
        pi.write(B2, 1)

        time.sleep(0.5)   

        pi.write(R2, 1)
        pi.write(G2, 0)
        pi.write(B2, 1)

        
        time.sleep(0.5)

        pi.write(R2, 1)
        pi.write(G2, 1)
        pi.write(B2, 0) 
except KeyboardInterrupt:
    pi.write(R1, 1)
    pi.write(G1, 1)
    pi.write(B1, 1)
    pi.write(R2, 1)
    pi.write(G2, 1)
    pi.write(B2, 1) 

  




