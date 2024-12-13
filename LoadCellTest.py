from machine import Pin
from hx711 import HX711
from time import sleep

# Pin configuration
DT = 17  # GPIO17 for data
SCK = 16  # GPIO16 for clock

# Initialize HX711
hx = HX711(d_out=DT, pd_sck=SCK)
hx.tare()  # Reset the scale to zero

# Set calibration factor (adjust based on your scale and setup)
hx.set_scale(-7050) #Need to calibrate

print("Scale is ready. Place weight on it.")

while True:
    try:
        weight = hx.get_units(10)  # Average of 10 readings
        print(f"Weight: {weight:.2f} grams")
        sleep(1)
    except KeyboardInterrupt:
        print("Exiting...")
        break