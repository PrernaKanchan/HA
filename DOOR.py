import  firebase_admin
from  firebase_admin import  credentials
from  firebase_admin import  db

import  sys
from  time import  sleep


import  signal
import gpiozero  
from  threading import Thread 


cred =  credentials . Certificate ( '/home/pi/smartcontrol-35c8b-firebase-adminsdk-yqtev-bc917cb4b5.json')
firebase_admin . initialize_app ( cred ,  {
    'databaseURL' : 'https://smartcontrol-35c8b.firebaseio.com/' 
})

RELAY_PIN = 21


REF_HOME = 'home'
REF_button = 'button'
REF_door = 'door_lock'
relay = gpiozero.OutputDevice(RELAY_PIN, active_high=False, initial_value=False)

class  IOT ():


    def  __init__ ( self ):
        self.refHome = db.reference(REF_HOME)
        self.button = self.refHome.child(REF_button)
        self.door_lock = self.button.child(REF_door) 
		
    def ledControlGPIO(self, status):
        if status:
            relay.on()
            print('Door open')
        else:
            relay.off()
            print('Door close')

    def buttonStart(self):

        E, i = [], 0

        status_previous = self.door_lock.get()
        self.ledControlGPIO(status_previous)

        E.append(status_previous)

        while True:
          status_actual = self.door_lock.get()
          E.append(status_actual)

          if E[i] != E[-1]:
              self.ledControlGPIO(status_actual)

          del E[0]
          i = i + i
          sleep(0.4)

print ('START !')
iot = IOT()

subprocess_led = Thread(target=iot.buttonStart)
subprocess_led.daemon = True
subprocess_led.start()
signal.pause()
