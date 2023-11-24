import os
import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QTimer, QThread, QObject, pyqtSignal, QEventLoop
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap, QImage

from six.moves.queue import Queue
# from threading import *

from generate_html import generate_html
from generate_pdf import generate_pdf
from plotter import Plotter

import serial
import spidev

spi = spidev.SpiDev()
spi.open(0, 0)  # Use CE0 (Chip Enable 0) for the SPI communication
spi.max_speed_hz = 5000000  # You may need to adjust this based on your sensor's specifications
# import modbus_tk.defines as cst
# from modbus_tk import modbus_rtu

import time
import RPi.GPIO as GPIO

import numpy as np
import pandas as pd

from random import random

characterized_pump = {
    "pump_type": "",
    "service_order" : "", 
    "date" : "", 
    "delegate" : "", 
    "model" : "",

    "motor_speed" : 0, 
    "power" : 0, 
    "parking_slot" : 0,
    "test_number" : 0,
    
    "flow" : [], 
    "pressure" : [], 
    "velocity" : [], 
    "elevation" : [], 
    "pump_total" : [], 
    "pump_power" : [], 
    "pump_efficiency" : [],
    "final_flow" : 0,
    "final_head" : 0, 
    "final_efficiency" : 0,
    "total_measurements": 0
}


# water_density_df = pd.read_excel("data/density/Densidad_agua.xlsx") # Load table for water densities at different temperatures

water_propierties_df = pd.read_excel("data/water_propierties/Propiedades_agua.xlsx") # Load table for water densities at different temperatures



# ADC I2C communication ******************************************************************************

import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Initialize the I2C interface
i2c = busio.I2C(board.SCL, board.SDA)

# Create an ADS1115 object
ads = ADS.ADS1115(i2c)

import modbus_tk.defines as cst
from modbus_tk import modbus_rtu

# Wattmeters ***************************************************
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

measuring_presure = False

pressure_in_global = 0
pressure_out_global = 0

# !adc = Adafruit_ADS1x15.ADS1115()

class Window(QtWidgets.QMainWindow):
    def __init__(self, path, screen_width):
        super(Window,self).__init__()
        loadUi(path,self)
        self.screen_width = screen_width

        self.defineFontSizes(self.centralwidget)

        # Green button pin definitions    ******************************************************************************
        # Green button pin definitions    ******************************************************************************


        
        self.green_button_pin = 27
        # GPIO.setup(self.green_button_pin, GPIO.IN)
        
    def defineFontSizes(self, main_object):

        text_font_size = self.screen_width // 80
        title_font_size = self.screen_width // 64
        button_font_size = self.screen_width // 106

        if main_object.layout() is None:
            return 0
        
        for i in range(main_object.layout().count()):
            element = main_object.layout().itemAt(i)
            if type(element) is QtWidgets.QWidgetItem :
                if "label" or "li_" in element.widget().objectName():
                    element.widget().setStyleSheet(f''' font-size: {text_font_size}px; ''')

                if "title" in element.widget().objectName():
                    element.widget().setStyleSheet(f''' font-size: {title_font_size}px; ''')
                
                if "Button" in element.widget().objectName():
                    element.widget().setStyleSheet(f''' font-size: {button_font_size}px; ''')
                
                if "alerts" in element.widget().objectName():
                    element.widget().setStyleSheet(f''' font-size: {int(title_font_size * 3/2)}px; color: red''')
                if "logo" in element.widget().objectName():
                    pixmap_image = QPixmap("data/imgs/logo.png")
                    element.widget().setPixmap(pixmap_image.scaledToWidth(self.screen_width // 6))
                    element.widget().setAlignment(Qt.AlignCenter)
            self.defineFontSizes(element)


class FirstWindow(Window):
    def __init__(self, path, screen_width):
        super().__init__(path, screen_width)
        self.pushButton.clicked.connect(self.goToNextTask)
        self.alerts.setText("Seleccione un tipo de bomba y diligencie las casillas")
        self.alerts.setStyleSheet(f''' color: green ''')

        # GPIO.add_event_detect(self.green_button_pin, GPIO.RISING, callback = self.goToNextTask, bouncetime = 2000)
    
    def goToNextTask(self):
        

        if self.roto.isChecked():
            characterized_pump["pump_type"] = "roto"
            widget.setCurrentIndex(1)
        elif self.triplex.isChecked():
            characterized_pump["pump_type"] = "triplex" 

            # GPIO.remove_event_detect(self.green_button_pin)
            # GPIO.add_event_detect(self.green_button_pin, GPIO.RISING, callback = widget.widget(1).goToNextTask, bouncetime = 2000)
            widget.setCurrentIndex(1)
            # GPIO.add_event_detect(self.green_button_pin, GPIO.RISING, callback = widget.currentWidget().goToNextTask, bouncetime = 2000)
            currentWidget()
        else:
            self.alerts.setText("Debe seleccionar un tipo de bomba")
            self.alerts.setStyleSheet(f''' color: red ''')


        characterized_pump["service_order"] = self.lE_1_service_order.text()
        characterized_pump["delegate"] = self.lE_2_delegate.text()
        characterized_pump["date"] = self.lE_3_date.text()
        characterized_pump["model"] = self.lE_4_pump_model.text()
        characterized_pump["total_measurements"] = int(self.measurements.text())

class SecondWindow(Window):
    def __init__(self, path, screen_width):
        super().__init__(path, screen_width)

        self.alerts.setText("Abra la válvula totalmente")
        self.alerts.setStyleSheet(f''' color: green ''')
        

        self.label_fo.setStyleSheet(f"font-size: {self.screen_width // 80}px; background-color: lightgreen")
        self.label_fo.hide()
        self.lcdNumber_fo.hide()
        self.label_fo_units.hide()

        self.pushButton.clicked.connect(self.goToNextTask)

        self.flowmeter_pulses = 0
        
        self.actual_flow = 0
        self.flow_measurement_started = False
        self.start_time_flow_measurement = 0
        self.flow = 0
        self.pulses_per_liter = 0 #! Define conversion factor

        self.max_flow = 0

        # self.pressure_in = 0 #! May be don't needed
        # self.pressure_out = 0
        # self.power = 0
        # self.temperature = 0

        self.actual_step = 0
        self.progressBar.setMaximum(100)
        self.progressBar.setValue(0)

        self.different_apertures = [0, 0, 0, 0, 0]

        self.timer = QTimer(self)
        self.timer_flow_measurement = QTimer(self)

        self.timer.timeout.connect(self.defineButtonState)
        self.timer.timeout.connect(self.showSensorsData)
        self.timer.start(1000)

        # self.timer_flow_measurement.timeout.connect(self.definingFlow)
        # self.timer_flow_measurement.start(500)

        # self.flow_measurement_time = 10 # sec
        self.max_flow_was_defined = False

        
    def defineButtonState(self):
        # Hold pushButton disabled while a requirement is not achieved
        if len(self.different_apertures) > 0 and len(self.different_apertures) > self.actual_step // 2:# and self.actual_step != 1:
            if self.flow >= self.different_apertures[self.actual_step // 2]:
                self.pushButton.setEnabled(True)

        # self.contador_random += 1

    def goToNextTask(self):
        print(f"actual_step: {self.actual_step // 2}")

        # If all the measurements were taken, then go to next screen
        if self.actual_step // 2 == characterized_pump["total_measurements"]:
            # GPIO.remove_event_detect(self.green_button_pin)
            # GPIO.add_event_detect(self.green_button_pin, GPIO.RISING, callback = widget.widget(2).goToNextTask, bouncetime = 2000)
            widget.setCurrentIndex(2)
            return
        
        # If the push button is not enabled, do not allow to execute the routines.
        # This is necessary for the physical button connected to the Raspberry Pi
        if not self.pushButton.isEnabled():
            return

        print(f"Medición actual: {self.actual_step}")
        
        if self.actual_step == -1:
                
            self.alerts.setText("Abra la válvula completamente")
            self.alerts.setStyleSheet(f''' color: green ''')

            self.actual_step += 1

        elif self.actual_step == 0:
                
            self.alerts.setText("¡¡¡Espere!!! Midiendo caudal máximo")
            self.alerts.setStyleSheet(f''' color: blue ''')
            # Whe the valve is completely open, take tha measured flow as the maximum flow
            self.pushButton.setEnabled(False)
            # QTimer.singleShot(self.flow_measurement_time * 1000, self.enableButtonAfterFMeasurement)
            
            self.actual_step += 1

        elif self.actual_step % 2 == 0:
            # Show in screen the target flow
            self.label_fo.show()
            self.lcdNumber_fo.show()
            self.label_fo_units.show()
            
            # Define target flow
            target_flow = round(self.different_apertures[self.actual_step // 2] , 2)

            # Show alerts to guide the search process of the target flow
            self.alerts.setText(f"Cierre la válvula hasta obtener flujo de {target_flow } L/min")
            self.lcdNumber_fo.display(target_flow)
            self.alerts.setStyleSheet(f''' color: green ''')
            self.pushButton.setEnabled(False)
            
            self.actual_step += 1


        elif self.actual_step % 2 == 1:

            # Hide the target flow
            self.label_fo.hide()
            self.lcdNumber_fo.hide()
            self.label_fo_units.hide()

            self.pushButton.setEnabled(False)

            self.thread1 = QThread()

            self.check_stability_on_thread = checkStabilityOnThread()
            self.check_stability_on_thread.moveToThread(self.thread1)

            self.thread1.started.connect(self.check_stability_on_thread.check)
            self.check_stability_on_thread.finished.connect(self.thread1.quit)
            self.check_stability_on_thread.finished.connect(self.check_stability_on_thread.deleteLater)
            self.thread1.finished.connect(self.thread1.deleteLater)
            self.check_stability_on_thread.progress.connect(self.reportProgress)
            self.check_stability_on_thread.flag.connect(self.checkFinished)
                    
            self.thread1.start() 

            # self.thread1.finished.connect(
            #     lambda: self.pushButton.setEnabled(True)
            # )

            # self.storeMeasurement()

    def enableButtonAfterFMeasurement(self):
        self.pushButton.setEnabled(True)

        # Define the apertures for each measurement point
        self.max_flow = self.flow
        self.different_apertures = self.max_flow * np.linspace(1, 0.3, characterized_pump["total_measurements"])

        self.alerts.setText("Caudal máximo medido. Continue con el proceso")
        self.alerts.setStyleSheet(f''' color: green ''')

    def reportProgress(self, n): #! Test function, it should be deleted
        # self.alerts.setText(f"Time: {n}")
        self.alerts.setText("¡¡¡Espere!!! Midiendo estabilidad")
        self.alerts.setStyleSheet(f''' color: blue ''')

    def checkFinished(self, check_flag):
        if check_flag:
            self.alerts.setText("Se ha hallado la estabilidad. Continue con el proceso")
            self.alerts.setStyleSheet(f''' color: green ''')
            self.pushButton.setEnabled(True)
            
            bar_value = int((self.actual_step // 2 + 1) / characterized_pump["total_measurements"] * 100)
            self.lcd_measurement.display(self.actual_step // 2 + 1)
            self.progressBar.setValue(bar_value)
            self.progressBar.setFormat("%.02f %%" % bar_value)


            self.thread2 = QThread()

            self.measure_on_thread = measureOnThread()
            self.measure_on_thread.moveToThread(self.thread2)

            self.thread2.started.connect(self.measure_on_thread.measurementsAverage)
            self.measure_on_thread.finished.connect(self.thread2.quit)
            self.measure_on_thread.finished.connect(self.measure_on_thread.deleteLater)
            self.thread2.finished.connect(self.thread2.deleteLater)
            self.measure_on_thread.measurements_ready.connect(self.storeMeasurement)
            
            self.thread2.start() 
            # self.measure_on_thread.flag.connect(self.measurementsAverageFinished)

            self.actual_step += 1
        else:
            self.alerts.setText("No se ha podido hallar estabilidad")
            self.alerts.setStyleSheet(f''' color: red ''')

    # def measurementsAverageFinished(self):

    def showSensorsData(self):
        if not measuring_presure:
            pressure_in, pressure_out = measureAveragePressure() # self.measurePressure()
            self.lcdNumber_pin.display(pressure_in * 14.503773773)
            self.lcdNumber_pout.display(pressure_out * 14.503773773)
        # Display sensors data on screen
        self.lcdNumber_f.display(self.flow) #! Modify with the pump dictionary
        
        self.lcdNumber_pw.display(self.measurePower())
        self.lcdNumber_t.display(20) #self.measureTemperature())

        # print(f"flow: {self.flow}") 
        # print(f"pressure_in: {pressure_in}")
        # print(f"pressure_out: {pressure_out}")

        
    def storeMeasurement(self, measurements): #! Run it in a thread ---------------------------------------------------------------
        
        # pressure_in, pressure_out = measureAveragePressure()
        # electrical_power = self.measurePower()
        # temperature = 20 # self.measureTemperature()

        pressure_in = measurements[0] # Measurementes come from class measureOnThread method measurementsAverage
        pressure_out = measurements[1]
        electrical_power = measurements[2]
        temperature = measurements[3]
        

        z1 = 0
        z2 = 0
        suction_tube_area = 1
        discharge_tube_area = 1

        flow_velocity_suction = 0
        flow_velocity_discharge = 0

        suction_loses = 0
        discharge_loses = 0
        

        """ while time.time() - start_time < 2:
            pressure_in += 0 # adc.read_adc(sensor_1_pin, gain=gain) * (4.096/32767) #! * 14.503773773 to psi
            pressure_out += 0 # adc.read_adc(sensor_2_pin, gain=gain) * (4.096/32767) #! * 14.503773773 to psi
            # electrical_power += self.measurePower()
            # temperature += self.measureTemperature()

            measurements_counter += 1 """

        """ pressure_in /= measurements_counter
        pressure_out /= measurements_counter
        electrical_power /= measurements_counter
        temperature /= measurements_counter """

        # Loses **********************

        e_mang_trans = 0.0020 * 10 ** (-3) # m
        e_mang_neg = 0.001 * 10 ** (-3) # m
        water_viscosity = 0 # m^2/s
        g = 9.798 # m/s^2

        
        
        water_propierties = water_propierties_df[water_propierties_df['Temp. [°C]'] == temperature]

        water_density = float(water_propierties_df['Densidad [kg/m3]'].iloc[0])

        water_viscosity = float(water_propierties_df['Viscocidad cinematica [m²/s]'].iloc[0])

        
        g = 9.798

        if characterized_pump["pump_type"] == "roto":            
            z1 = 0.97
            z2 = 1.625
            suction_tube_area = ((51.8 * 10 ** (-3)) / 2) ** 2 * np.pi # m^2
            discharge_tube_area = ((38.8 * 10 ** (-3)) / 2) ** 2 * np.pi # m^2

            flow_velocity_suction   = self.flow / suction_tube_area   / 60000 # m/s
            flow_velocity_discharge = self.flow / discharge_tube_area / 60000 # m/s

            # Loses for rotodynamic pumps

            # Suction
            L_s = 0.5 # m
            D_s = 51.8 * 10 ** (-3) # m
            sum_k_s = 11.65 + 0.05
            e_s = e_mang_trans
            
            # Discharge loses 
            D_d_r = 38.8 / 25.4 # in
            sum_k_d_r = 11.65 + 1.5 + 1.4 * (D_d_r ** (-0.53))
            
            discharge_loses = (sum_k_d_r) * flow_velocity_discharge ** 2 / (2*g) # m

        elif characterized_pump["pump_type"] == "triplex": 
            z1 = 0.48
            z2 = 0.61
            suction_tube_area = ((24.8 * 10 ** (-3)) / 2) ** 2 * np.pi # m^2
            discharge_tube_area = ((10.75 * 10 ** (-3)) / 2) ** 2 * np.pi # m^2

            flow_velocity_suction   = self.flow / suction_tube_area   / 60000 # m/s
            flow_velocity_discharge = self.flow / discharge_tube_area / 60000 # m/s

            # Loses for triplex pumps

            # Suction
            L_s = 2.3 # m
            D_s = 24.8 * 10 ** (-3) # m
            sum_k_s = 0.3
            e_s = e_mang_trans

            # Discharge

            L_d_h = 3 # m
            D_d_h = 7 * 10 ** (-3) # m
            e_d_h = e_mang_neg
            
            f_d_h = self.haalandCalculations(e_d_h, D_d_h, water_viscosity, flow_velocity_discharge)
            discharge_loses = (f_d_h * (L_d_h / D_d_h)) * flow_velocity_discharge ** 2 / (2*g) # m
            

        
        

        velocity_head_1 = (flow_velocity_suction  )**2 / (2*g) # m
        velocity_head_2 = (flow_velocity_discharge)**2 / (2*g) # m

        # Suction loses ****************************
        f_s = self.haalandCalculations(e_s, D_s, water_viscosity, flow_velocity_suction)
        suction_loses = (f_s * (L_s / D_s) + sum_k_s) * flow_velocity_suction ** 2 / (2*g) # m 


        
    
        # suction_loses = 0 #! Cambiar después
        # discharge_loses = 0
        total_suction_head   = z1 + pressure_in * (100000) / (water_density * g) + velocity_head_1 - suction_loses
        total_discharge_head = z2 + pressure_out * (100000)/ (water_density * g) + velocity_head_2 + discharge_loses
        
        print("CABEZAS ============================================")
        print(f"total_suction_head: {total_suction_head}")
        print(f"total_discharge_head: {total_discharge_head}")

        pump_total = total_discharge_head - total_suction_head

        characterized_pump["flow"].append(self.flow)
        characterized_pump["pressure"].append(pressure_out * (14.5038))
        characterized_pump["velocity"].append(velocity_head_2 - velocity_head_1)
        characterized_pump["elevation"].append(z2 - z1)
        characterized_pump["pump_total"].append(pump_total)
        characterized_pump["pump_power"].append(electrical_power)

        hydraulic_power = water_density * g *  pump_total * self.flow * (1 / 60000) 
        characterized_pump["pump_efficiency"].append(hydraulic_power / electrical_power * 100)
        
        print("DATOS ALMACENADOS **********************************")
        print(characterized_pump)

        print("-------------------------------------------------------")

    def haalandCalculations(self, e, D, water_viscosity, V):
        Re = (D * V) / (water_viscosity)
        f_raiz = (-1.8 * np.log((( e / D) / 3.7) ** 1.11 + (6.9 / (Re + 0.000001)))) ** (-1) #! Delete the epsilon
        return f_raiz ** 2

    def measurePower(self):

        data = master.execute(1, cst.READ_INPUT_REGISTERS, 0, 10)
        power = (data[3] + (data[4] << 16)) / 10.0 # [W]
        data_2 = master2.execute(1, cst.READ_INPUT_REGISTERS, 0, 10)
        power_2 = (data_2[3] + (data_2[4] << 16)) / 10.0 # [W]

        active_power = power + power_2

        return active_power

    def measureTemperature(self):

        if characterized_pump["pump_type"] == "roto":
            cs_pin = 8

        if characterized_pump["pump_type"] == "triplex": 
              # Use any available GPIO pin
            cs_pin = 7
        else:
            cs_pin = 8
        
        return self.read_max6675(cs_pin)
        

        
    def read_max6675(self, cs_pin):
        # Set the Chip Select (CS) line for the selected MAX6675
        GPIO.output(cs_pin, GPIO.LOW)
        
        # Read raw data from MAX6675
        raw_data = spi.xfer2([0x00, 0x00])
        
        # Convert raw data to temperature in Celsius
        temperature = ((raw_data[0] << 8) | raw_data[1]) >> 3
        temperature *= 0.25  # Each bit represents 0.25 degrees Celsius
        
        # Release the Chip Select (CS) line
        GPIO.output(cs_pin, GPIO.HIGH)
        
        return temperature

    """ def measurePressure(self):
        
        factor_1 = 0 
        factor_2 = 0
        adc_read_1 = AnalogIn(ads, ADS.P1)
        adc_read_2 = AnalogIn(ads, ADS.P2)

        if characterized_pump["pump_type"] == "roto":
            adc_read_1 = AnalogIn(ads, ADS.P1) 
            adc_read_2 = AnalogIn(ads, ADS.P2)
            factor_1 = 13 / 4
            factor_2 =  25 / 4


        if characterized_pump["pump_type"] == "triplex": 
            adc_read_1 = AnalogIn(ads, ADS.P2)
            adc_read_2 = AnalogIn(ads, ADS.P3)
            factor_1 = 13 / 4
            factor_2 =  400 / 4

        pressure_in  = (adc_read_1.voltage - 0.6) * factor_1  - 1
        pressure_out = (adc_read_2.voltage - 0.6) * factor_2
        # factor_1=0
        # factor_2=0
        # if characterized_pump["pump_type"] == "roto":
        #     factor_1=13/1023 
        #     factor_2=25/1023              
        #     ser.write(b"R\n")

        # if characterized_pump["pump_type"] == "triplex": 
        #     factor_1=13/1023 
        #     factor_2=400/1023 
        #     ser.write(b"T\n")
        
        # # time.sleep(1)
        # try:
        #     arduino_data = ser.readline().decode('utf-8').rstrip()

            
        #     if arduino_data == "Arduino ready": 
        #         print(arduino_data)
        #         arduino_data = ser.readline().decode('utf-8').rstrip()
        #     if arduino_data == "":
        #         pressure_in = -1
        #         arduino_data = ser.readline().decode('utf-8').rstrip()
        #     else:
        #         try:
        #             pressure_in = float(arduino_data) * factor_1 - 1
        #             print("pressure_in:", pressure_in)
        #         except ValueError:
        #             print("Invalid data received:", arduino_data)
        #             pressure_in = 0
        # except serial.SerialException as e:
        #     print("Serial Exception:", e)
        #     pressure_in = 0
        

            
        # try:
        #     arduino_data2 = ser.readline().decode('utf-8').rstrip()
            
            
        #     if arduino_data2 == "Arduino ready": 
        #         print(arduino_data2)
        #         arduino_data2 = ser.readline().decode('utf-8').rstrip()
        #     if arduino_data2 == "":
        #         pressure_out = -1
        #         arduino_data2 = ser.readline().decode('utf-8').rstrip()
        #     else:
        #         try:
        #             pressure_out = float(arduino_data2) * factor_2
        #             print("pressure_out:", pressure_out)
        #         except ValueError:
        #             print("Invalid data received:", arduino_data2)
        #             pressure_out = 0
        # except serial.SerialException as e:
        #     print("Serial Exception:", e)
        #     pressure_out = 0

        return pressure_in, pressure_out """

    def countingFlowPulses(self, channel):

        if not self.flow_measurement_started:
            self.flow_measurement_started = True
            self.start_time_flow_measurement = time.time()
            self.flowmeter_pulses += 1
            # print(f"Pulse number: {self.flowmeter_pulses}")
        else:
            # print(f"Pulse number: {self.flowmeter_pulses}")
            self.flowmeter_pulses += 1
            
            if self.flowmeter_pulses == 3:
                self.definingFlow()

    def definingFlow(self):
        
        # if time.time() - self.start_time_flow_measurement >= self.flow_measurement_time and self.flow_measurement_started:
        self.flow = ((self.flowmeter_pulses - 1)/ (time.time() - self.start_time_flow_measurement) ) * 60
        self.flow_measurement_started = False
        self.flowmeter_pulses = 0

        # print(f"Tiempo de inicio: {self.flow_measurement_started}")
        # print(f"Tiempo final: {time.time()}")
        # print(f"Pulse number: {self.flowmeter_pulses}")
        # print(f"Diferencia de tiempo: {time.time() - self.start_time_flow_measurement}")
        # print(f"Flujo final: {self.flow}")

        if not self.max_flow_was_defined and self.actual_step == 1:
            self.enableButtonAfterFMeasurement()
            self.max_flow_was_defined = True
            # print(self.flow) 

    def wait(self, milliseconds):
        loop = QEventLoop()
        QTimer.singleShot(milliseconds, loop.quit)
        loop.exec_()

def measureAveragePressure():

    # measuring_presure = True

    factor_1 = 0 
    factor_2 = 0
    

    if characterized_pump["pump_type"] == "roto":
        # adc_read_1 = AnalogIn(ads, ADS.P1)
        # adc_read_2 = AnalogIn(ads, ADS.P2)

        pin_1 = ADS.P1
        pin_2 = ADS.P2
        factor_1 = 13 / 4
        factor_2 =  25 / 4


    elif characterized_pump["pump_type"] == "triplex": 
        # adc_read_1 = AnalogIn(ads, ADS.P2)
        # adc_read_2 = AnalogIn(ads, ADS.P3)
        pin_1 = ADS.P2
        pin_2 = ADS.P3
        factor_1 = 13 / 4
        factor_2 =  400 / 4
    else:
        pin_1 = ADS.P1
        pin_2 = ADS.P2

    try:
        adc_read_1 = AnalogIn(ads, pin_1)
        adc_read_2 = AnalogIn(ads, pin_2)

        pressure_in  = (adc_read_1.voltage - 0.6) * factor_1 - 1
        pressure_out = (adc_read_2.voltage - 0.63) * factor_2
        print(factor_2)
    except:
        pressure_in, pressure_out = measureAveragePressure()

        
    # measuring_presure = False

    return pressure_in, pressure_out

    
def measurePower():

    data = master.execute(1, cst.READ_INPUT_REGISTERS, 0, 10)
    power = (data[3] + (data[4] << 16)) / 10.0 # [W]
    data_2 = master2.execute(1, cst.READ_INPUT_REGISTERS, 0, 10)
    power_2 = (data_2[3] + (data_2[4] << 16)) / 10.0 # [W]

    active_power = power + power_2

    return active_power

def measureTemperature():

    if characterized_pump["pump_type"] == "roto":
        cs_pin = 8

    if characterized_pump["pump_type"] == "triplex": 
            # Use any available GPIO pin
        cs_pin = 7
    else:
        cs_pin = 8
    
    return self.read_max6675(cs_pin)
    

    
def read_max6675(cs_pin):
    # Set the Chip Select (CS) line for the selected MAX6675
    GPIO.output(cs_pin, GPIO.LOW)
    
    # Read raw data from MAX6675
    raw_data = spi.xfer2([0x00, 0x00])
    
    # Convert raw data to temperature in Celsius
    temperature = ((raw_data[0] << 8) | raw_data[1]) >> 3
    temperature *= 0.25  # Each bit represents 0.25 degrees Celsius
    
    # Release the Chip Select (CS) line
    GPIO.output(cs_pin, GPIO.HIGH)
    
    return temperature


class checkStabilityOnThread(QObject):

    finished = pyqtSignal()
    
    progress = pyqtSignal(float)
    flag = pyqtSignal(bool)

    def check(self):
        
        gain = 1
        if characterized_pump["pump_type"] == "roto": #!Change pin numbers            
            sensor_1_pin = 0
            sensor_2_pin = 0

        if characterized_pump["pump_type"] == "triplex": #!Change pin numbers
            sensor_1_pin = 0
            sensor_2_pin = 0

        average_m_1 = 0
        average_m_2 = 0
        data_counter = 0
        start_count_stabilization_time = time.time()
        start_checking_process_time = time.time()

        while True:
            
            checking_time = time.time() - start_checking_process_time
            self.progress.emit(round(checking_time, 2))

            pressure_1 = 0 # adc.read_adc(sensor_1_pin, gain=gain) * (4.096/32767)
            pressure_2 = 0 # adc.read_adc(sensor_2_pin, gain=gain) * (4.096/32767)

            average_m_1 += pressure_1
            average_m_2 += pressure_2

            data_counter += 1

            # Search for unstable values
            if abs(pressure_1 - average_m_1/data_counter) > 0.06 * average_m_1/data_counter or abs(pressure_2 - average_m_2/data_counter) > 0.06 * average_m_2/data_counter:
                average_m_1 = 0
                average_m_2 = 0
                data_counter = 0
                start_count_stabilization_time = time.time()

                if time.time() - start_checking_process_time >= 60:
                    self.flag.emit(False)
                    self.finished.emit()
                    break
            
            if time.time() - start_count_stabilization_time >= 1:
                
                self.flag.emit(True)
                self.finished.emit()
                break
    
    

class measureOnThread(QObject):
    finished = pyqtSignal()
    measurements_ready = pyqtSignal(list)

    def measurementsAverage(self):
        
        
        measurements_counter = 0
        start_time = time.time()

        pressure_in = 0
        pressure_out = 0
        electrical_power = 0
        temperature = 0
        measuring_presure = True
        while time.time() - start_time < 5:

            p_in, p_out = measureAveragePressure()

            pressure_in += p_in # pressure_in = pressure_in + p_in 
            pressure_out += p_out

            electrical_power += measurePower()
            temperature += 20
            measurements_counter += 1



            # if abs(pressure_out / measurements_counter - p_out) > pressure_out * 0.06:

            #     break
            
            time.sleep(1)
            

            
        measuring_presure = False
        pressure_in /= measurements_counter
        pressure_out /= measurements_counter
        electrical_power /= measurements_counter
        temperature /= measurements_counter
        self.measurements_ready.emit([pressure_in, pressure_out, electrical_power, temperature])
        self.finished.emit()



            
class ThirdWindow(Window):
    def __init__(self, path, screen_width):
        super().__init__(path, screen_width)
        self.pushButton.clicked.connect(self.goToNextTask)
        self.progressBar.setValue(0)
        self.alerts.setText("Listo para generar el reporte")
        self.alerts.setStyleSheet(f''' color: green ''')
        self.count_button_pushed = 0

    
    def goToNextTask(self):

        self.count_button_pushed += 1
        
        if self.count_button_pushed >= 2:
            # GPIO.remove_event_detect(self.green_button_pin)
            # GPIO.add_event_detect(self.green_button_pin, GPIO.RISING, callback = widget.widget(0).goToNextTask, bouncetime = 2000)
            widget.setCurrentIndex(0)
            return

        self.alerts.setText("Generando reporte")

        # characterized_pump["flow"] = [1,2,3,4,5]
        # characterized_pump["pressure"] =  [55, 54.5, 54, 53, 52.5, 51.7, 50, 48.5, 46, 44]
        # characterized_pump["velocity"] =  [1,2,3,4,5,6,7,8,9,10]
        # characterized_pump["elevation"] =  [1,2,3,4,5,6,7,8,9,10]
        # characterized_pump["pump_total"] =  [1,2,3,4,5,6,7,8,9,10]
        # characterized_pump["pump_power"] =  [6,12,14,20,22]
        # characterized_pump["pump_efficiency"] =  [0,10,20,20,25,30,40,70,60,50]
        
        # Finding most efficient point
        index = characterized_pump["pump_efficiency"].index(max(characterized_pump["pump_efficiency"])) 
        characterized_pump["final_flow"] =  characterized_pump["flow"][index]
        characterized_pump["final_head"] =  characterized_pump["pressure"][index]
        characterized_pump["final_efficiency"] =  characterized_pump["pump_efficiency"][index]

        self.progressBar.setValue(20)

        # Generate the graphs of power, pressure, efficiency vs flow

        
        flow_vs_pump_power = Plotter(characterized_pump["flow"], characterized_pump["pump_power"],"Flujo vs Potencia","Flujo (L/min)","Potencia (kW)", "FlowVsPower.png")
        flow_curve, power_curve = flow_vs_pump_power.plotter()
        self.progressBar.setValue(30)


        flow_vs_pressure = Plotter(characterized_pump["flow"], characterized_pump["pump_total"],"Flujo vs Cabeza","Flujo (L/min)","Cabeza (m)", "FlowVsHead.png")
        _, head_curve = flow_vs_pressure.plotter()
        self.progressBar.setValue(40)
        
        flow_vs_pump_efficiency = Plotter(characterized_pump["flow"], characterized_pump["pump_efficiency"],"Flujo vs Eficiencia" ,"Flujo (L/min)","Eficiencia (%)", "FlowVsEfficiency.png")
        flow_vs_pump_efficiency.plotter()


        # f = open('example.txt', 'w')

        

        # hydraulic_power_curve = 998.8 * 9.798 *  head_curve * flow_curve * (1 / 60000) 

        # efficiency_curve = hydraulic_power_curve / power_curve

        # with open('readme.txt', 'w') as f:
        #     f.write(hydraulic_power_curve)
        #     f


        # flow_vs_pump_efficiency.plotInterpolatedCurves(flow_curve, efficiency_curve)
        self.progressBar.setValue(50)

        # Generate a html file that is going to be used as a base for the pdf generation
        generate_html(characterized_pump)
        self.progressBar.setValue(70)

        # Generate the final report in pdf
        generate_pdf(characterized_pump["test_number"])
        self.progressBar.setValue(100)

        self.alerts.setText("Generación de reporte finalizado")

        self.pushButton.setText("Caracterizar otra bomba")


        
 #! Una idea para poder lidiar con las interrupciones de GPIO en caso de que hayan problemas       
""" class GpioThread(QThread):
    event_detected = pyqtSignal(int)
    def __init__(self, *args, **kwargs):
        QThread.__init__(self, *args, **kwargs)
        self.queue = Queue()
        GPIO.add_event_detect(channel, GPIO.BOTH, callback=self.queue.put)

    def run(self):
        while True:
            self.event_detected.emit(self.queue.get()) """






def closeApp(widget):
    widget.close()
    os.system("shutdown now") #shut down the Pi -h is or -r will reset

def turnOnLed(led_pin):

    GPIO.output(led_pin,GPIO.HIGH)



if __name__ == '__main__':

    GPIO.setmode(GPIO.BCM)
    # ser = serial.Serial('/dev/ttyACM0', 115200, timeout=0)
    # ser.reset_input_buffer()

    app = QtWidgets.QApplication(sys.argv)

    screen = app.primaryScreen()
    screen_width = screen.availableGeometry().width()
    screen_height = screen.availableGeometry().height()

    # widget.setFixedWidth(screen_width)
    # widget.setFixedHeight(screen_height)

    widget = QtWidgets.QStackedWidget()
    information_window = FirstWindow("Information_screen.ui", screen_width)
    # information_window.pushButton.clicked.connect(getInformation)
    widget.addWidget(information_window)

    measurements_window = SecondWindow("Measurements_screen.ui", screen_width)
    widget.addWidget(measurements_window)

    # Flowmeter pins definition     ******************************************************************************

    if characterized_pump["pump_type"] == "roto":
        flowmeter_pin = 4 #! Definir bien los pines
    elif characterized_pump["pump_type"] == "triplex":
        flowmeter_pin = 17
    else:
        flowmeter_pin = 4
    #measurements_window.start_timer.connect(measurements_window.countFlowTime)
    
    GPIO.setup(flowmeter_pin, GPIO.IN)
    
    GPIO.add_event_detect(flowmeter_pin, GPIO.RISING, callback = measurements_window.countingFlowPulses, bouncetime = 500)

    # Temperature pins              ******************************************************************************
    # Set the GPIO pins for the Chip Select (CS) lines to OUTPUT
    GPIO.setup(8, GPIO.OUT)
    GPIO.setup(7, GPIO.OUT)

    
    

    # Red button pin definitions    ******************************************************************************

    red_button_pin = 23 # Button to close the app
    GPIO.setup(red_button_pin, GPIO.IN)
    print(str(GPIO.input(23)))
    # GPIO.add_event_detect(red_button_pin, GPIO.RISING, callback = lambda x: closeApp(widget))

    green_led_pin = 0 #! Define pins
    GPIO.setup(green_led_pin,GPIO.OUT)

    red_led_pin = 0
    GPIO.setup(red_led_pin,GPIO.OUT)

    report_generation_window = ThirdWindow("Generate_Report.ui", screen_width)
    widget.addWidget(report_generation_window)

    widget.show()



    sys.exit(app.exec_())

