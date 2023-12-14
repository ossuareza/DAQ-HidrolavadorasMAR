# First Code

# https://electrocredible.com/raspberry-pi-pico-max6675-thermocouple/

""" from max6675 import MAX6675
from machine import Pin
import time



sensor = MAX6675(sck, cs , so)

while True:
    print("temperature=")
    print(sensor.read())
    time.sleep(1)
 """

# Another option (Writing the class)

# https://diyprojectslab.com/max6675-with-raspberry-pi-pico/





""" 
from max6675 import MAX6675
import time

# Define the GPIO pins for your MAX6675 sensors
cs_pin_1 = 17  # Use the appropriate GPIO pin
cs_pin_2 = 18  # Use another appropriate GPIO pin

# Create instances for each MAX6675 sensor
max6675_1 = MAX6675(cs_pin_1)
max6675_2 = MAX6675(cs_pin_2)

try:
    while True:
        temperature_1 = max6675_1.get()
        temperature_2 = max6675_2.get()
        
        if temperature_1 is not None:
            print(f"Sensor 1 Temperature: {temperature_1}Â°C")
        else:
            print("Error reading from Sensor 1")

        if temperature_2 is not None:
            print(f"Sensor 2 Temperature: {temperature_2}Â°C")
        else:
            print("Error reading from Sensor 2")

        time.sleep(1)  # You can adjust the polling interval as needed

except KeyboardInterrupt:
    pass """



import RPi.GPIO as GPIO
import spidev
import time

# Set up SPI communication



# sck = Pin(11, Pin.OUT) # GPIO 11 pin 23
# cs = Pin(8, Pin.OUT) # GPIO 8 pin 24
# so = Pin(9, Pin.IN) # GPIO 9 pin 21

# GPIO pin numbers for the Chip Select (CS) lines for each MAX6675
cs_pin_1 = 0  # Use any available GPIO pin
cs_pin_2 = 1  # Use another available GPIO pin

# Function to read temperature from MAX6675
def read_max6675(cs_pin):
    spi = spidev.SpiDev()
    spi.open(0, cs_pin)  # Use CE0 (Chip Enable 0) for the SPI communication
    spi.max_speed_hz = 5000000  # You may need to adjust this based on your sensor's specifications
    # Set the Chip Select (CS) line for the selected MAX6675
 
    
    # Read raw data from MAX6675
    raw_data = spi.xfer2([0x00, 0x00])
    
    # Convert raw data to temperature in Celsius
    temperature = ((raw_data[0] << 8) | raw_data[1]) >> 3
    temperature *= 0.25  # Each bit represents 0.25 degrees Celsius
    
    # Release the Chip Select (CS) line
    #GPIO.output(cs_pin, GPIO.LOW)
    spi.close()
    return temperature

try:
  
    
    while True:
        temperature_1 = read_max6675(cs_pin_1)
        temperature_2 = read_max6675(cs_pin_2)
       
        
        print(f"Sensor 1 Temperature: {temperature_1} °C")
        print(f"Sensor 2 Temperature: {temperature_2} °C")
        
        time.sleep(1)  # You can adjust the polling interval as needed

except KeyboardInterrupt:
    pass

# Cleanup GPIO
GPIO.cleanup()

# Close SPI connection