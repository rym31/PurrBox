import pigpio
import time

BTN = 16 
pi = pigpio.pi()
etat = -1
prev = -1

NIVEAU_ROBUSTESSE = 5
try:
  
    while True:
        while True:
            etat = pi.read(BTN)
            # print(etat)
            if etat != prev:
                somme = 0
                isNew = True
                for i in range(NIVEAU_ROBUSTESSE):
                    if pi.read(BTN) != etat:
                        isNew = False
                        break
                    time.sleep(0.01)
                if isNew: 
                    prev = etat
                    if etat == 0:
                        print("click")
                        
                        
                        
                            
            time.sleep(0.02)
    
except KeyboardInterrupt:
    print("Au revoir!")

finally:
    pi.stop()