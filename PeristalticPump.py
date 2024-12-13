import time
from machine import Pin

pump = Pin(38, Pin.OUT)

def pump_on():
    pump.value(1) 

def pump_off():
    pump.value(0) 

def pump_pulse(duration):
    pump_on()
    time.sleep(duration)
    pump_off() 

while True:
    pump_pulse(1)

