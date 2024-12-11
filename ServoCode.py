from machine import pin, PWM
servo = PWM(Pin(38), freq=50)
while True:
    servo.duty(360)