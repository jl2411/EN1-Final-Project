from machine import Pin, PWM
import time
servo = PWM(Pin(37), freq=50)
while True:
    servo.duty(20)
    time.sleep(0.5)
    servo.duty(130)
    time.sleep(0.5)

