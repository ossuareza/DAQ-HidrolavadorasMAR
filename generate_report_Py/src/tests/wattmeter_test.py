# =========================================================================================
#
# Debugging 
# https://amitasinghchauhan.medium.com/serial-port-debugging-101-loopback-test-4a7e40da9055
#
# =========================================================================================

import time

# https://www.youtube.com/watch?v=oevxqPk78sM


#library for LED matrix
# from luma.led_matrix.device import max7219
# from luma.core.interface.serial import spi, noop
# from luma.core.render import canvas
# from luma.core.virtual import viewport
# from luma.core.legacy import text, show_message, textsize
# from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT

#library for PZEM-004T V3
import serial
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu

#Setting LED matrix
# serial_led = spi(port=0, device=0, gpio=noop())
# device = max7219(serial_led, cascaded=4, block_orientation=-90)


# Connect to the slave
wattmeter_1 = serial.Serial(
                       port='/dev/ttyS0',
                       baudrate=9600,
                       bytesize=8,
                       parity='N',
                       stopbits=1,
                       xonxoff=0
                      )

master = modbus_rtu.RtuMaster(wattmeter_1)
master.set_timeout(2.0)
master.set_verbose(True)

wattmeter_2 = serial.Serial(
                       port='/dev/ttyAMA5',
                       baudrate=9600,
                       bytesize=8,
                       parity='N',
                       stopbits=1,
                       xonxoff=0
                      )

master2 = modbus_rtu.RtuMaster(wattmeter_2)
master2.set_timeout(2.0)
master2.set_verbose(True)


wattmeter_3 = serial.Serial(
                       port='/dev/ttyAMA2',
                       baudrate=9600,
                       bytesize=8,
                       parity='N',
                       stopbits=1,
                       xonxoff=0
                      )

master3 = modbus_rtu.RtuMaster(wattmeter_3)
master3.set_timeout(2.0)
master3.set_verbose(True)



while True:
	data = master.execute(1, cst.READ_INPUT_REGISTERS, 0, 10)
	voltage = data[0] / 10.0 # [V]
	current = (data[1] + (data[2] << 16)) / 1000.0 # [A]
	power = (data[3] + (data[4] << 16)) / 10.0 # [W]
	energy = data[5] + (data[6] << 16) # [Wh]
	frequency = data[7] / 10.0 # [Hz]
	powerFactor = data[8] / 100.0
	alarm = data[9] # 0 = no alarm

	print('Voltage [V]\t: ', voltage)
	print('Current [A]\t: ', current)
	print('Power [W]\t: ', power) # active power (V * I * power factor)
	# print('Energy [Wh]\t: ', energy)
	# print('Frequency [Hz]\t: ', frequency)
	# print('Power factor []\t: ', powerFactor)


	data2 = master2.execute(1, cst.READ_INPUT_REGISTERS, 0, 10)
	voltage2 = data2[0] / 10.0 # [V]
	current2 = (data2[1] + (data2[2] << 16)) / 1000.0 # [A]
	power2 = (data2[3] + (data2[4] << 16)) / 10.0 # [W]
	energy2 = data2[5] + (data2[6] << 16) # [Wh]
	frequency2 = data2[7] / 10.0 # [Hz]
	powerFactor2 = data2[8] / 100.0
	alarm2 = data2[9] # 0 = no alarm
	# print("Segundaaaaaaaaaaaaaaaaa")
	print('Voltage 2 [V]\t: ', voltage2)
	print('Current 2 [A]\t: ', current2)
	print('Power 2 [W]\t: ', power2) # active power (V * I * power factor)


	data3 = master3.execute(1, cst.READ_INPUT_REGISTERS, 0, 10)
	voltage3 = data3[0] / 10.0 # [V]
	current3 = (data3[1] + (data3[2] << 16)) / 1000.0 # [A]
	power3 = (data3[3] + (data3[4] << 16)) / 10.0 # [W]
	energy3 = data3[5] + (data3[6] << 16) # [Wh]
	frequency3 = data3[7] / 10.0 # [Hz]
	powerFactor3 = data3[8] / 100.0
	alarm3 = data3[9] # 0 = no alarm
	# print("Segundaaaaaaaaaaaaaaaaa")
	print('Voltage 3 [V]\t: ', voltage3)
	print('Current 3 [A]\t: ', current3)
	print('Power 3 [W]\t: ', power3) # active power (V * I * power factor)

	

	print("=====================================")

	time.sleep(1)
	# print("Potencia activa:", power + power2)
	# print('Energy [Wh]\t: ', energy2)
	# print('Frequency [Hz]\t: ', frequency2)
	# print('Power factor []\t: ', powerFactor2)
	#print('Alarm : ', alarm)
	# print("--------------------")

	#show Ampere in LED matrix
	# msg = str(current)
	# w, h = textsize(msg, font=proportional(CP437_FONT))
	# x = round((device.width - w) / 2)
	# with canvas(device) as draw:
	# 	text(draw, (x, 0), msg, fill="white", font=proportional(CP437_FONT))
	
	time.sleep(1)

# Changing power alarm value to 100 W
# master.execute(1, cst.WRITE_SINGLE_REGISTER, 1, output_value=100)

try:
    master.close()
    if slave.is_open:
        slave.close()
except:
   pass


# Second code trying with serial

import time
import json
import serial
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu
# if __name__ == "__main__":
#     try:
#         # Connect to the slave
#         serial = serial.Serial(
#                                port='/dev/ttyS0',
#                                baudrate=9600,
#                                bytesize=8,
#                                parity='N',
#                                stopbits=1,
#                                xonxoff=0
#                               )
#         master = modbus_rtu.RtuMaster(serial)
#         master.set_timeout(2.0)
#         master.set_verbose(True)
#         # Changing power alarm value to 100 W 
#         # master.execute(1, cst.WRITE_SINGLE_REGISTER, 1, output_value=100)
#         dict_payload = dict()
#         while True:
#             data = master.execute(1, cst.READ_INPUT_REGISTERS, 0, 10)
#             dict_payload["voltage"]= data[0] / 10.0
#             dict_payload["current_A"] = (data[1] + (data[2] << 16)) / 1000.0 # [A]
#             dict_payload["power_W"] = (data[3] + (data[4] << 16)) / 10.0 # [W]
#             dict_payload["energy_Wh"] = data[5] + (data[6] << 16) # [Wh]
#             dict_payload["frequency_Hz"] = data[7] / 10.0 # [Hz]
#             dict_payload["power_factor"] = data[8] / 100.0
#             dict_payload["alarm"] = data[9] # 0 = no alarm
#             str_payload = json.dumps(dict_payload, indent=2)
#             print(str_payload)
#             time.sleep(1)
        
#     except KeyboardInterrupt:
#         print('exiting pzem script')
#     except Exception as e:
#         print(e)
#     finally:
#         master.close()


# {'pump_type': 'roto', 'service_order': '', 'date': '', 'delegate': '', 'model': '', 'motor_speed': 0, 'power': 0, 'parking_slot': 0, 'test_number': 0, 'flow': [80.10116638630319, 73.92332288923365, 68.59332413788593, 61.77781727326332, 58.89591502977347], 'pressure': [0.0, 30.426575092318497, 38.82317180486466, 44.602205979491565, 0.0], 'velocity': [0.04457904675219594, 0.037967854645320126, 0.03269014126651821, 0.026516623180021, 0.024100355261270856], 'elevation': [0.655, 0.655, 0.655, 0.655, 0.655], 'pump_total': [1.868426657638853, 24.060700214429072, 29.68524678026441, 33.364485958493226, 1.311046182831139], 'pump_power': [1.0, 1.0, 1.0, 1.0, 1.0], 'pump_efficiency': [0.0, 253218540.1590119, 299801508.9927236, 310205754.1528057, 0.0], 'final_flow': 0, 'final_head': 0, 'final_efficiency': 0, 'total_measurements': 5, 'pump_model': ''}
