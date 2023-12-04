# First code *************************************88
# https://how2electronics.com/how-to-use-ads1115-16-bit-adc-module-with-raspberry-pi/



import board
import busio
import  adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import time
 
# Initialize the I2C interface
i2c = busio.I2C(board.SCL, board.SDA)
 
# Create an ADS1115 object
ads = ADS.ADS1115(i2c)

# ads.mode = Mode.CONTINUOUS # This could make execution faster 
 
# Define the analog input channels
channel0 = AnalogIn(ads, ADS.P0)
channel1 = AnalogIn(ads, ADS.P1)
channel2 = AnalogIn(ads, ADS.P2)
channel3 = AnalogIn(ads, ADS.P3)
 
# Loop to read the analog inputs continuously
while True:
    print("Analog Value 0: ", channel0.value, "Voltage 0: ", channel0.voltage)
    print("Analog Value 1: ", channel1.value, "Voltage 1: ", channel1.voltage)
    print("Analog Value 2: ", channel2.value, "Voltage 2: ", channel2.voltage)
    print("Analog Value 3: ", channel3.value, "Voltage 3: ", channel3.voltage)

    print("=============================================")
    
    # Delay for 1 second
    time.sleep(2)


# Second code *********************************************

# https://www.engineersgarage.com/raspberry-pi-ads1015-ads1115-analog-sensor-interfacing-ir-sensor-interfacing/

# import Adafruit_ADS1x15

# gain = 1

# adc = Adafruit_ADS1x15.ADS1115()

# value0 = adc.read_adc(0, gain=gain)
# value1 = adc.read_adc(1, gain=gain)
# value2 = adc.read_adc(2, gain=gain)
# value3 = adc.read_adc(3, gain=gain)

# analog_voltage0 = value0*(4.096/32767)
# analog_voltage1 = value1*(4.096/32767)
# analog_voltage2 = value2*(4.096/32767)
# analog_voltage3 = value3*(4.096/32767)


