import time
import machine

# Define pin connections
pump_pin = machine.Pin(0, machine.Pin.OUT)  # Adjust this to match your pump pin

def pump_on():
    """Turns the peristaltic pump on."""
    pump_pin.value(1) 

def pump_off():
    """Turns the peristaltic pump off."""
    pump_pin.value(0) 

def pump_pulse(duration_ms):
    """
    Activates the pump for a specified duration (in milliseconds).
    """
    pump_on()
    time.sleep_ms(duration_ms)
    pump_off() 

# Example usage: 
# Pump for 1 second
pump_pulse(1000) 
