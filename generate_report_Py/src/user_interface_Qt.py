import os
import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QTimer, QThread, QObject, pyqtSignal, QEventLoop
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap, QImage

from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem, QHeaderView
import argparse
import json



# Define how the software id going to be executed

parser = argparse.ArgumentParser()

parser.add_argument('--testing_interface', action="store_true", help="Test the interface without sensors connections")

parser.add_argument('--testing_buttons', action="store_true", help="Test the physical buttons without sensors connections")

parser.add_argument('--not_use_wattmeter_1', action="store_true", help="Run the software with the wattmeter_1")
parser.add_argument('--not_use_wattmeter_2', action="store_true", help="Run the software with the wattmeter_2")
parser.add_argument('--not_use_wattmeter_3', action="store_true", help="Run the software with the wattmeter_3")
args = parser.parse_args()



testing_interface = args.testing_interface
testing_buttons = args.testing_buttons
use_wattmeter_1 = not args.not_use_wattmeter_1
use_wattmeter_2 = not args.not_use_wattmeter_2
use_wattmeter_3 = not args.not_use_wattmeter_3



from generate_html import generate_html
from generate_pdf import generate_pdf
from plotter import Plotter
from send_email import send_email

# If this is a interface test, unable the communication protocols, so you can test it without the raspberry or the sensors
if not testing_interface:
    import serial
    import spidev
    import RPi.GPIO as GPIO

    spi = spidev.SpiDev()

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

# import modbus_tk.defines as cst
# from modbus_tk import modbus_rtu

import time

import numpy as np
import pandas as pd

from random import random




if testing_buttons:
    testing_interface = True


# Define the data structure used to pass the information across the whole architecture


characterized_pump = {
    "pump_type": "",
    "motor_type": "",
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
    "total_measurements": 0,

    "temperature": 0
}



script_path = os.path.abspath(sys.argv[0])
src_path = os.path.dirname(script_path)
directory_path = os.path.dirname(src_path)



water_properties_path = os.path.join(directory_path, "data", "water_properties", "Propiedades_agua.xlsx")  # Load table for water densities at different temperatures
water_properties_df = pd.read_excel(water_properties_path) # Load table for water densities at different temperatures



# Definition of serial communication for the Wattmeters ***************************************************

if use_wattmeter_1 and not testing_interface:
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

if use_wattmeter_2 and not testing_interface:
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

if use_wattmeter_3 and not testing_interface:
    wattmeter_3 = serial.Serial(
                        port='/dev/ttyAMA3',
                        baudrate=9600,
                        bytesize=8,
                        parity='N',
                        stopbits=1,
                        xonxoff=0
                        )

    master3 = modbus_rtu.RtuMaster(wattmeter_3)
    master3.set_timeout(2.0)
    master3.set_verbose(True)




measuring_pressure = False


pressure_in_global = 0
pressure_out_global = 0





# !adc = Adafruit_ADS1x15.ADS1115()

from six.moves.queue import Queue
from PyQt5.QtCore import pyqtSlot as pyQtSlot

class RelayThread(QThread):
    event_detected = pyqtSignal(int)
    def __init__(self, channel):
        QThread.__init__(self)
        self.queue = Queue()

        if not testing_interface or testing_buttons:
            GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            # green_button_pin = 27 # Button to advance though the user interface
            # GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            # print(str(GPIO.input(channel)))
            GPIO.add_event_detect(channel, GPIO.BOTH, callback=self.queue.put_nowait, bouncetime = 100)

    def run(self):
        while True:
            self.event_detected.emit(self.queue.get())





class Window(QtWidgets.QMainWindow):
    def __init__(self, path, screen_width):
        super(Window,self).__init__()
        loadUi(path,self)
        self.screen_width = screen_width

        self.defineFontSizes(self.centralwidget)

        
    def defineFontSizes(self, main_object): # Adaptative size for text

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
                    image_path = os.path.join(directory_path, "data", "imgs", "logo.png")
                    pixmap_image = QPixmap(image_path)
                    element.widget().setPixmap(pixmap_image.scaledToWidth(self.screen_width // 6))
                    element.widget().setAlignment(Qt.AlignCenter)
            self.defineFontSizes(element)




class PyQt_RPI(Window):

    def __init__(self, widget):
        super(Window,self).__init__()
        self.relay_thread = RelayThread(27)
        self.relay_thread.event_detected.connect(self.on_gpio_event)
        self.relay_thread.start()
        self.widget_array = widget

        self.previous_state = None
        self.second_flank_detected_time = 0
        self.first_flank_detected_time = 0
        
        # self.green_button_pin = 27
        self.first_flank_detected_time = 0
        self.second_flank_detected_time = 0
        self.first_flank_detected = False


    @pyQtSlot(int)
    def on_gpio_event(self, channel):
        
        if time.time() - self.first_flank_detected_time > 2:
            self.first_flank_detected = False
        
        if self.first_flank_detected:
            # print("Second flank")
            self.second_flank_detected_time = time.time() - self.first_flank_detected_time
            print(self.second_flank_detected_time)
            if self.second_flank_detected_time >= 0.1 and self.second_flank_detected_time <= 2:
                print("Green button pressed.")
                QTimer.singleShot(200, widget.currentWidget().goToNextTask)

            self.first_flank_detected = False
            # second_flank_detected = True

        else:
            # print("First flank")
            self.first_flank_detected_time = time.time()
            self.first_flank_detected = True



        """ if self.previous_state is None:
            self.previous_state = GPIO.input(channel)
            self.first_flank_detected_time = time.time()
            

        else:
            current_state = GPIO.input(channel)
            #print(f"pin {4}: {str(GPIO.input(4))}")
            if current_state != self.previous_state:
                # Flank detected
                self.second_flank_detected_time = time.time()
            
            if self.second_flank_detected_time - self.first_flank_detected_time >= 0.8:
                # Signal has stayed in the new state for at least 1 second
                print("Red button pressed.")
                self.previous_state = None
                self.widget_array.currentWidget().goToNextTask()
                print("An event occurred on channel {}".format(channel))

            elif time.time() - self.first_flank_detected_time >= 3:
                return """
        
            

    


class FirstWindow(Window):
    def __init__(self, path, screen_width):
        super().__init__(path, screen_width)
        self.pushButton.clicked.connect(self.goToNextTask)
        self.alerts.setText("Seleccione un tipo de bomba y diligencie las casillas")
        self.alerts.setStyleSheet(f''' color: green ''')

        self.reset_enabled = False

        

    
    def goToNextTask(self,*channel):
        alert_message = ""
        alert_boolean = False

        global characterized_pump

        # Check if every box was filled in
        if (self.lE_1_service_order.text() == '' or self.lE_2_delegate.text() == '' or self.lE_3_date.text() == '' or self.lE_4_pump_model.text() == '' 
            or self.lE_5_motor_speed.text() == '' or self.lE_6_pump_power.text() == '' or self.lE_7_parking_slot.text() == ''):
            alert_message = "Debe diligenciar todos los campos \n"
            alert_boolean = True
            
        # Check which radio buttons were checked
        if self.roto.isChecked():
            characterized_pump["pump_type"] = "roto"
            
        elif self.triplex.isChecked():
            characterized_pump["pump_type"] = "triplex" 

        else:
            alert_message += "Debe seleccionar un tipo de bomba \n"
            alert_boolean = True

        if self.single_phase.isChecked():
            characterized_pump["motor_type"] = "single-phase"

        elif self.two_phase.isChecked():
            characterized_pump["motor_type"] = "two-phase"
            
        elif self.three_phase.isChecked():
            characterized_pump["motor_type"] = "three-phase" 
        

        else:
            alert_message += "Debe seleccionar un tipo de motor"
            alert_boolean = True

        # If there is something to be filled in, report the error
        if alert_boolean:
            print(alert_message)
            self.alerts.setText(alert_message)
            self.alerts.setStyleSheet(f''' color: red ''')
        
        else:
            characterized_pump["service_order"] = self.lE_1_service_order.text()
            characterized_pump["delegate"] = self.lE_2_delegate.text()
            characterized_pump["date"] = self.lE_3_date.text()
            characterized_pump["model"] = self.lE_4_pump_model.text()
            characterized_pump["motor_speed"] = self.lE_5_motor_speed.text()
            characterized_pump["power"] = self.lE_6_pump_power.text()
            characterized_pump["parking_slot"] = self.lE_7_parking_slot.text()

            if characterized_pump["pump_type"] == "roto":
                characterized_pump["total_measurements"] = int(self.measurements.text())
            elif characterized_pump["pump_type"] == "triplex": 
                characterized_pump["total_measurements"] = 3

            widget.setCurrentIndex(1) # Go to the next window

            


            print(f"Booleano de reseteo en Primera Ventana: {self.reset_enabled}")
            
            if self.reset_enabled: # Reset variables if asked
                    print("Reseteando Variables")
                    widget.currentWidget().resetVariables()
                    widget.currentWidget().progressBar.setValue(0)
                    self.reset_enabled = False
        


        
        

class SecondWindow(Window):
    def __init__(self, path, screen_width):
        super().__init__(path, screen_width)

        self.alerts.setText("Preparando el sistema, continue con el proceso")
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

        self.max_flow = 0

        self.time_between_pulses = []
        self.first_pulse_received = False
        self.last_pulse_received_time = 0
        self.new_bounce_time = 1

        self.actual_step = -1
        self.progressBar.setMaximum(100)
        self.progressBar.setValue(0)

        self.different_apertures = [0, 0, 0, 0, 0]

        self.timer = QTimer(self)
        
        
        self.flowmeter_pin = None

        self.timer.timeout.connect(self.defineButtonState)
        self.timer.timeout.connect(self.showSensorsData)
        self.timer.start(1000)

        self.max_flow_was_defined = False
        self.are_variables_reset = False

        self.searching_target = False


        # if not testing_interface:
        #     GPIO.setup(self.flowmeter_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        #     GPIO.add_event_detect(self.flowmeter_pin, GPIO.RISING, callback = self.detectPulses)

    def resetVariables(self):
        global characterized_pump 
        
        # if testing_interface:
        #     GPIO.remove_event_detect(self.flowmeter_pin)
        
        self.max_flow_was_defined = False
        self.flow_measurement_started = False
        self.flowmeter_pin = None

        characterized_pump["flow"] =  []
        characterized_pump["pressure"] =  []
        characterized_pump["velocity"] =  []
        characterized_pump["elevation"] =  []
        characterized_pump["pump_total"] =  []
        characterized_pump["pump_power"] =  []
        characterized_pump["pump_efficiency"] =  []
        characterized_pump["final_flow"] =  0
        characterized_pump["final_head"] =  0
        characterized_pump["final_efficiency"] =  0
        characterized_pump["temperature"] = 0
        
        
        self.alerts.setText("Preparando el sistema")
        self.alerts.setStyleSheet(f''' color: green ''')
        

        self.label_fo.setStyleSheet(f"font-size: {self.screen_width // 80}px; background-color: lightgreen")
        self.label_fo.hide()
        self.lcdNumber_fo.hide()
        self.label_fo_units.hide()

        # self.pushButton.clicked.connect(self.goToNextTask)

        self.flowmeter_pulses = 0
        
        self.actual_flow = 0
        self.start_time_flow_measurement = 0
        self.flow = 0
        
        self.max_flow = 0

        self.time_between_pulses = []
        self.first_pulse_received = False
        self.last_pulse_received_time = 0

        self.new_bounce_time = 1


        self.actual_step = -1

        self.lcd_measurement.display(0)

        self.progressBar.setMaximum(100)
        self.progressBar.setValue(0)
        self.progressBar.setFormat("%.02f %%" % 0)

        self.different_apertures = [0, 0, 0, 0, 0]

        self.timer = QTimer(self)

        self.timer.timeout.connect(self.defineButtonState)
        self.timer.timeout.connect(self.showSensorsData)
        self.timer.start(1000)

        self.are_variables_reset = True

        self.searching_target = False


        
    def defineButtonState(self):

        global characterized_pump

        # Hold pushButton disabled while a requirement is not achieved
        if len(self.different_apertures) > 0 and len(self.different_apertures) > self.actual_step // 2 and self.actual_step != 1:
            if self.searching_target and self.actual_step % 2 == 1:
                if ((self.flow >= self.different_apertures[self.actual_step // 2] * 0.9 and self.flow <= self.different_apertures[self.actual_step // 2] * 1.1)
                    or characterized_pump["pump_type"] != "roto"):
                    # and (self.actual_step % 2 == 0 or self.actual_step == 1):
                    self.pushButton.setEnabled(True)
                else:
                    self.pushButton.setEnabled(False)
            elif self.actual_step % 2 != 1:
                self.pushButton.setEnabled(True)
        
        if testing_interface:
            self.pushButton.setEnabled(True)

        # self.contador_random += 1

    def goToNextTask(self):

        global characterized_pump

        print(f"actual_step: {self.actual_step // 2}")
        # print(characterized_pump)
        # if self.flow < 40:
        #     GPIO.remove_event_detect(flowmeter_pin)
        #     GPIO.add_event_detect(flowmeter_pin, GPIO.RISING, callback = self.goToNextTask, bouncetime = 1500)

        # If all the measurements were taken, then go to next screen
        if self.actual_step == 2 * characterized_pump["total_measurements"]:
            # GPIO.remove_event_detect(self.green_button_pin)
            # GPIO.add_event_detect(self.green_button_pin, GPIO.RISING, callback = widget.widget(2).goToNextTask, bouncetime = 2000)
            widget.setCurrentIndex(2)
            # print(widget.currentWidget(), "()" * 40)
            widget.currentWidget().goToNextTask()
            
            if not testing_interface:
                GPIO.remove_event_detect(self.flowmeter_pin)
            return



        # If the push button is not enabled, do not allow to execute the routines.
        # This is necessary for the physical button connected to the Raspberry Pi
        if not self.pushButton.isEnabled():
            return

        # print(f"Medición actual: {self.actual_step}")
        
        self.searching_target = False

        if self.actual_step == -1:
            
            if self.are_variables_reset:
            #     if not testing_interface:
            #         GPIO.remove_event_detect(self.flowmeter_pin)
                self.are_variables_reset = False

            self.flowmeter_pin = 24
            
            if characterized_pump["pump_type"] == "roto":
                self.flowmeter_pin = 24 
                self.new_bounce_time = 1
                # print("Caudalímetro de las bombas rotodinámicas")

            elif characterized_pump["pump_type"] == "triplex":
                self.flowmeter_pin = 17
                self.new_bounce_time = 3
                # print("Caudalímetro de las bombas triplex")
            
            print("FLOWMETERPIN: ", self.flowmeter_pin)
            if not testing_interface:
                GPIO.setup(self.flowmeter_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
                GPIO.add_event_detect(self.flowmeter_pin, GPIO.RISING, callback = self.detectPulses)    

            self.alerts.setText("Abra la válvula completamente y espere a que aparezca \n el caudal máximo")
            self.alerts.setAlignment(Qt.AlignCenter)
            self.alerts.setStyleSheet(f''' color: green ''')

            self.actual_step += 1

        elif self.actual_step == 0:
                
            self.alerts.setText("¡¡¡Espere!!! Midiendo caudal máximo")
            self.alerts.setStyleSheet(f''' color: blue ''')
            # When the valve is completely open, take tha measured flow as the maximum flow
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

            if characterized_pump["pump_type"] == "roto":  
                self.alerts.setText(f"Cierre la válvula hasta obtener flujo de {target_flow } \u00B1 {round(target_flow * 0.1, 2)} L/min")
            elif characterized_pump["pump_type"] == "triplex":
                self.alerts.setText(f"Intente obtener un flujo de {target_flow } L/min")
            self.lcdNumber_fo.display(target_flow)
            self.alerts.setStyleSheet(f''' color: green ''')
            
            self.searching_target = True
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

    def enableButtonAfterFMeasurement(self):

        global characterized_pump


        self.pushButton.setEnabled(True)

        if characterized_pump["pump_type"] == "triplex":

            min_aper_percentage = 0.7

        else:
            min_aper_percentage = 0.45

        # Define the apertures for each measurement point
        self.max_flow = self.flow
        self.different_apertures = self.max_flow * np.linspace(1, min_aper_percentage, characterized_pump["total_measurements"])

        self.alerts.setText("Caudal máximo medido. Continue con el proceso")
        self.alerts.setStyleSheet(f''' color: green ''')

    def reportProgress(self, n): 
        # self.alerts.setText(f"Time: {n}")
        self.alerts.setText("¡¡¡Espere!!! Midiendo estabilidad")
        self.alerts.setStyleSheet(f''' color: blue ''')

    def checkFinished(self, check_flag):

        global characterized_pump

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

            self.actual_step += 1
        else:
            self.alerts.setText("No se ha podido hallar estabilidad")
            self.alerts.setStyleSheet(f''' color: red ''')
            time.sleep(1)

    def showSensorsData(self):

        if testing_interface:
            
            return

        if not measuring_pressure:
            pressure_in, pressure_out = measurePressure() # self.measurePressure()
            self.lcdNumber_pin.display(pressure_in * 14.503773773)
            self.lcdNumber_pout.display(pressure_out * 14.503773773)
        # Display sensors data on screen
        self.lcdNumber_f.display(self.flow)
        power, current = measurePower()
        self.lcdNumber_pw.display(power)
        self.lcdNumber_c.display(current)
        self.lcdNumber_t.display(  measureTemperature() if not testing_interface else 20)



        
    def storeMeasurement(self, measurements): 

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

        # Loses **********************

        e_mang_trans = 0.0020 * 10 ** (-3) # m
        e_mang_neg = 0.001 * 10 ** (-3) # m
        water_viscosity = 0 # m^2/s
        g = 9.798 # m/s^2

        
        try:        
            water_properties = water_properties_df[water_properties_df['Temp. [°C]'] == temperature]

            water_density = float(water_properties['Densidad [kg/m3]'].iloc[0])

            water_viscosity = float(water_properties['Viscocidad cinematica [m²/s]'].iloc[0])
        except:
            water_density = 997.8

            water_viscosity = 0.0000009565

            print("FALLO LEYENDO MEDICIÓN DE TEMPERATURA. Temperatura = ", temperature)
        
        g = 9.798

        global characterized_pump

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


        total_suction_head   = z1 + pressure_in * (100000) / (water_density * g) + velocity_head_1 - suction_loses
        total_discharge_head = z2 + pressure_out * (100000)/ (water_density * g) + velocity_head_2 + discharge_loses
        # print("PERDIDAS ============================================")
        # print(f"suction_loses: {suction_loses}")
        # print(f"discharge_loses: {discharge_loses}")
        # print("PRESIONES ============================================")
        # print(f"pressure_in: {pressure_in}")
        # print(f"pressure_out: {pressure_out}")
        # print("CABEZAS ============================================")
        # print(f"total_suction_head: {total_suction_head}")
        # print(f"total_discharge_head: {total_discharge_head}")

        pump_total = total_discharge_head - total_suction_head

        characterized_pump["flow"].append(self.flow)
        characterized_pump["pressure"].append(pressure_out * (14.5038))
        characterized_pump["velocity"].append(velocity_head_2 - velocity_head_1)
        characterized_pump["elevation"].append(z2 - z1)
        characterized_pump["pump_total"].append(pump_total)
        characterized_pump["pump_power"].append(electrical_power)

        characterized_pump["temperature"] = temperature

        hydraulic_power = water_density * g *  pump_total * self.flow * (1 / 60000) 
        characterized_pump["pump_efficiency"].append(hydraulic_power / electrical_power * 100)
        
        

        print("-------------------------------------------------------")

    def haalandCalculations(self, e, D, water_viscosity, V):
        Re = (D * V) / (water_viscosity)
        f_raiz = (-1.8 * np.log((( e / D) / 3.7) ** 1.11 + (6.9 / (Re + 0.000001)))) ** (-1) #! Delete the epsilon
        return f_raiz ** 2


    def detectPulses(self, channel):
    

        if self.new_bounce_time is not None:

            if abs(time.time() - self.last_pulse_received_time) > self.new_bounce_time:
                
                self.countingFlowPulses()
        else:
            self.countingFlowPulses()


        # Start counting the time between pulses
        if not self.first_pulse_received:
            self.first_pulse_received = True
            self.last_pulse_received_time = time.time()

        # Store the time between pulses, so you can look for a pattern
        elif self.last_pulse_received_time != 0:
            self.time_between_pulses.append(time.time() -  self.last_pulse_received_time)
            self.last_pulse_received_time = time.time()

        if len(self.time_between_pulses) > 4:
            self.new_bounce_time = sum(self.time_between_pulses[-4:]) / 4 # Take the new bounce time as the average of the times stored

            # ANOTHER ALTERNATIVES
            # new_bounce_time = max(time_between_pulses[-4:])

    def countingFlowPulses(self):
        print(" ========  flow_measurement_started: ", self.flow_measurement_started)
        print(" ********  max_flow_was_defined: ", self.max_flow_was_defined)
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

        if not self.max_flow_was_defined and self.actual_step == 1:
            self.enableButtonAfterFMeasurement()
            self.max_flow_was_defined = True

    def wait(self, milliseconds):
        loop = QEventLoop()
        QTimer.singleShot(milliseconds, loop.quit)
        loop.exec_()


# Measuring Functions ************************************************************************************************************

def measurePressure():

    # measuring_pressure = True

    global characterized_pump

    factor_1 = 0 
    factor_2 = 0
    pin_1 = ADS.P0
    pin_2 = ADS.P1
    offset_1 = 0
    offset_2 = 0
    

    if characterized_pump["pump_type"] == "roto":
        pin_1 = ADS.P2
        pin_2 = ADS.P3
        factor_1 = 13 / (4.905 - 0.713)
        factor_2 =  25 / (4.8197 - 0.6421)

        offset_1 = 0.713
        offset_2 = 0.6421


    elif characterized_pump["pump_type"] == "triplex": 
        pin_1 = ADS.P0
        pin_2 = ADS.P1
        factor_1 = 13 / (4.8224 - 0.456) 
        factor_2 =  400 / (4.7382 - 0.6726)

        offset_1 = 0.456
        offset_2 = 0.6726

    try:
        adc_read_1 = AnalogIn(ads, pin_1)
        adc_read_2 = AnalogIn(ads, pin_2)
        
        

        pressure_in  = (adc_read_1.voltage - offset_1) * factor_1 - 1
        pressure_out = (adc_read_2.voltage - offset_2) * factor_2
    except:
        pressure_in, pressure_out = measurePressure()

        
    # measuring_pressure = False

    return pressure_in, pressure_out

    
def measurePower():

    global characterized_pump

    if characterized_pump['motor_type'] == 'single-phase':

        if use_wattmeter_2:
            data_2 = master2.execute(1, cst.READ_INPUT_REGISTERS, 0, 10)
            power_2 = (data_2[3] + (data_2[4] << 16)) / 10.0 # [W]
            current_2 = (data_2[1] + (data_2[2] << 16)) / 1000.0 # [A]

        if use_wattmeter_2:
            active_power = power_2
            current = current_2
        else:
            active_power = 0
            current = 0

    elif characterized_pump['motor_type'] == 'two-phase':
        if use_wattmeter_1 and use_wattmeter_2 and use_wattmeter_3:
            data = master.execute(1, cst.READ_INPUT_REGISTERS, 0, 10)
            power_1 = (data[3] + (data[4] << 16)) / 10.0 # [W]
            
            data_2 = master2.execute(1, cst.READ_INPUT_REGISTERS, 0, 10)
            power_2 = (data_2[3] + (data_2[4] << 16)) / 10.0 # [W]
            current_2 = (data_2[1] + (data_2[2] << 16)) / 1000.0 # [A]
            
            data_3 = master3.execute(1, cst.READ_INPUT_REGISTERS, 0, 10)
            
            power_3 = (data_3[3] + (data_3[4] << 16)) / 10.0 # [W]

            power_list = [power_1, power_2, power_3]
            power_list.sort(reverse=True)

            active_power = power_list[0] + power_list[1]

            power_factor = 0.86

            voltage_list = [data[0] / 10.0, data_2[0] / 10.0, data_3[0] / 10.0]
            voltage_list.sort(reverse=True)

            current = ((active_power / 2) / power_factor) / voltage_list[0]
            
        
        else:
            active_power = 0
            current = 0



    elif characterized_pump['motor_type'] == 'three-phase':

        if use_wattmeter_1 and use_wattmeter_2 and use_wattmeter_3:
            data = master.execute(1, cst.READ_INPUT_REGISTERS, 0, 10)
            power_1 = (data[3] + (data[4] << 16)) / 10.0 # [W]
            
            data_2 = master2.execute(1, cst.READ_INPUT_REGISTERS, 0, 10)
            power_2 = (data_2[3] + (data_2[4] << 16)) / 10.0 # [W]
            current_2 = (data_2[1] + (data_2[2] << 16)) / 1000.0 # [A]
            
            data_3 = master3.execute(1, cst.READ_INPUT_REGISTERS, 0, 10)
            
            power_3 = (data_3[3] + (data_3[4] << 16)) / 10.0 # [W]

            active_power = power_1 + power_2 + power_3

            power_factor = 0.86
            V_L_3 = data_3[0] / 10.0 # [V]
            current = ((active_power / 3) / power_factor) / V_L_3
            
        
        else:
            active_power = 0
            current = 0
    
    else:
        active_power = 0
        current = 0

    return active_power, current

def measureTemperature():

    global characterized_pump

    if characterized_pump["pump_type"] == "roto":
        cs_pin = 1

    elif characterized_pump["pump_type"] == "triplex": 
        cs_pin = 0
    else:
        cs_pin = 0
    
    return round(read_max6675(cs_pin))
    

    
def read_max6675(cs_pin):
    
    spi.open(0, cs_pin)  # Use CE0 (Chip Enable 0) for the SPI communication
    spi.max_speed_hz = 5000000  # You may need to adjust this based on your sensor's specifications
    
    # Read raw data from MAX6675
    raw_data = spi.xfer2([0x00, 0x00])
    
    spi.close()
    # Convert raw data to temperature in Celsius
    temperature = ((raw_data[0] << 8) | raw_data[1]) >> 3
    temperature *= 0.25  # Each bit represents 0.25 degrees Celsius
    
    if temperature < 15 and cs_pin == 0:
        if read_max6675(1) > 15:
            temperature = measureTemperature()

            
    return temperature


class checkStabilityOnThread(QObject):

    finished = pyqtSignal()
    
    progress = pyqtSignal(float)
    flag = pyqtSignal(bool)

    def check(self):
        
        average_m_1 = 0
        average_m_2 = 0
        data_counter = 0
        start_count_stabilization_time = time.time()
        start_checking_process_time = time.time()

        while True and not testing_interface:
            
            checking_time = time.time() - start_checking_process_time
            self.progress.emit(round(checking_time, 2))

            pressure_1, pressure_2 = measurePressure()

            average_m_1 += pressure_1
            average_m_2 += pressure_2

            data_counter += 1
            
            # print("No se ha hallado estabilidad =============================================")
            # print("Presure_in: ", pressure_1)
            # print("Presure_out: ", pressure_2)
            # print("Presure_in_M: ", average_m_1)
            # print("Presure_out_M: ", average_m_2)
            # print("ERROR_1: ", pressure_1 - average_m_1/data_counter)
            # print("ERROR_2: ", pressure_2 - average_m_2/data_counter)

            

            # Search for unstable values
            if abs(pressure_1 - average_m_1/data_counter) > abs(0.5 * average_m_1/data_counter) or abs(pressure_2 - average_m_2/data_counter) > abs(0.5 * average_m_2/data_counter):
                average_m_1 = 0
                average_m_2 = 0
                data_counter = 0
                start_count_stabilization_time = time.time()
                

                if time.time() - start_checking_process_time >= 60:
                    self.flag.emit(False)
                    self.finished.emit()
                    break
            
            if time.time() - start_count_stabilization_time >= 10:
                
                self.flag.emit(True)
                self.finished.emit()
                break
        
        if testing_interface:
            self.flag.emit(True)
            self.finished.emit()
    

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
        measuring_pressure = True
        while time.time() - start_time < 1 :

            if testing_interface:
                measurements_counter += 1
                break

            p_in, p_out = measurePressure()

            pressure_in += p_in # pressure_in = pressure_in + p_in 
            pressure_out += p_out

            power, _ = measurePower()
            electrical_power += power
            temperature += measureTemperature()
            measurements_counter += 1



            # if abs(pressure_out / measurements_counter - p_out) > pressure_out * 0.06:

            #     break
            
            # time.sleep(1)
            

            
        measuring_pressure = False

        if testing_interface:
            pressure_in = 0
            pressure_out = 0
            electrical_power = 0
            temperature = 0

        else:
            pressure_in /= measurements_counter
            pressure_out /= measurements_counter
            electrical_power /= measurements_counter

            temperature /= measurements_counter
        self.measurements_ready.emit([pressure_in, pressure_out, electrical_power, round(temperature)])
        self.finished.emit()


class ThirdWindow(Window):
    
    def __init__(self, path, screen_width):
        super().__init__(path, screen_width)
        self.pushButton_1.clicked.connect(self.goToNextTask)
        self.pushButton_2.clicked.connect(self.resetMeasurementProcess)
        self.count_button_pushed = 0

    def addTableRow(self, table, row_data):
            row = table.rowCount()
            table.setRowCount(row+1)
            col = 0
            for item in row_data:
                cell = QTableWidgetItem(str(item))
                table.setItem(row, col, cell)
                col += 1
    
    def clearTable(self, table):
        while (table.rowCount() > 0):

            table.removeRow(0)
    
    def goToNextTask(self):
        print("Entrando a la ventana de resuemen" + "=" * 20)
        # print(widget.currentWidget(), "()" * 40)
        print(self.count_button_pushed)

        global characterized_pump

        self.label_7.setText (characterized_pump["service_order"])
        self.label_12.setText(characterized_pump["delegate"])
        self.label_13.setText(characterized_pump["date"])
        self.label_14.setText(characterized_pump["model"])
        self.label_15.setText(characterized_pump["motor_speed"] + "  RPM")
        self.label_16.setText(characterized_pump["power"] + "  W")
        self.label_17.setText(characterized_pump["parking_slot"])
        self.label_18.setText(str(characterized_pump["total_measurements"]))



        self.tableWidget.setColumnCount(characterized_pump['total_measurements'] + 1)

        self.tableWidget.rowCount()
        #set table header
        print( "==" * 30)
        print(characterized_pump)

        self.tableWidget.setHorizontalHeaderLabels(['Variable'] + [str(i) for i in range(1, characterized_pump["total_measurements"] + 1)])

        self.addTableRow(self.tableWidget, ["Flujo (L/m)"] + [round(element) for element in characterized_pump["flow"]])
        self.addTableRow(self.tableWidget, ["Presión (psi)"] + [round(element) for element in characterized_pump["pressure"]])
        self.addTableRow(self.tableWidget, ["Potencia (W)"] + [round(element) for element in characterized_pump["pump_power"]])
        # self.addTableRow(self.tableWidget, row_4)
    
        hheader = self.tableWidget.horizontalHeader()
        hheader.setSectionResizeMode(QHeaderView.ResizeToContents)

        self.count_button_pushed += 1
        
        if self.count_button_pushed >= 2:
            self.count_button_pushed = 0
            
            print("Cambio a la generación de PDF")
            widget.setCurrentIndex(3)
            
            self.clearTable(self.tableWidget)

            keys = ["service_order", "delegate", "date", "model", "motor_speed", "power", "parking_slot"]
            line_edit = [self.lineEdit_1, self.lineEdit_2, self.lineEdit_3, self.lineEdit_4, self.lineEdit_5, self.lineEdit_6, self.lineEdit_7 ]

            for i, key in zip(range(7), keys):
                if line_edit[i].text() != "":
                    characterized_pump[key] = line_edit[i].text()

            
            
    def resetMeasurementProcess(self):
        
        self.count_button_pushed = 0
        widget.setCurrentIndex(0)
            
        widget.currentWidget().reset_enabled = True

        print(f"Booleano de reseteo en Tercera Ventana: {widget.currentWidget().reset_enabled}")

        widget.currentWidget().alerts.setText("Seleccione un tipo de bomba y diligencie las casillas")
        widget.currentWidget().alerts.setStyleSheet(f''' color: green ''')

        widget.currentWidget().lE_1_service_order.setText("")
        widget.currentWidget().lE_2_delegate.setText("")
        widget.currentWidget().lE_3_date.setText("")
        widget.currentWidget().lE_4_pump_model.setText("")
        widget.currentWidget().lE_5_motor_speed.setText("")
        widget.currentWidget().lE_6_pump_power.setText("")
        widget.currentWidget().lE_7_parking_slot.setText("")
        widget.currentWidget().measurements.setValue(5)

        self.count_button_pushed = 0
            

        
        

            
class FourthWindow(Window):
    def __init__(self, path, screen_width):
        super().__init__(path, screen_width)
        self.pushButton.clicked.connect(self.goToNextTask)
        self.progressBar.setValue(0)
        self.alerts.setText("Listo para generar el reporte")
        self.alerts.setStyleSheet(f''' color: green ''')
        self.count_button_pushed = 0


    


    
    def goToNextTask(self):

        global characterized_pump
        
        self.count_button_pushed += 1
        
        if self.count_button_pushed >= 2:
            # GPIO.remove_event_detect(self.green_button_pin)
            # GPIO.add_event_detect(self.green_button_pin, GPIO.RISING, callback = widget.widget(0).goToNextTask, bouncetime = 2000)
            widget.setCurrentIndex(0)
            
            widget.currentWidget().reset_enabled = True
            print(f"Booleano de reseteo en Cuarta Ventana: {widget.currentWidget().reset_enabled}")

            widget.currentWidget().alerts.setText("Seleccione un tipo de bomba y diligencie las casillas")
            widget.currentWidget().alerts.setStyleSheet(f''' color: green ''')

            widget.currentWidget().lE_1_service_order.setText("")
            widget.currentWidget().lE_2_delegate.setText("")
            widget.currentWidget().lE_3_date.setText("")
            widget.currentWidget().lE_4_pump_model.setText("")
            widget.currentWidget().lE_5_motor_speed.setText("")
            widget.currentWidget().lE_6_pump_power.setText("")
            widget.currentWidget().lE_7_parking_slot.setText("")
            widget.currentWidget().measurements.setValue(5)

            widget.currentWidget().roto.setChecked(False)
            # widget.currentWidget().triplex.setChecked(False)
            widget.currentWidget().single_phase.setChecked(False)
            widget.currentWidget().two_phase.setChecked(False)
            # widget.currentWidget().three_phase.setChecked(False)

            self.count_button_pushed = 0
            self.progressBar.setValue(0)
            self.pushButton.setText("Generar Reporte")
            
            return

        self.pushButton.setEnabled(False)
        self.alerts.setText("Generando reporte")
        
        # Finding most efficient point

        if not testing_interface:
            index = characterized_pump["pump_efficiency"].index(max(characterized_pump["pump_efficiency"])) 
            characterized_pump["final_flow"] =  characterized_pump["flow"][index]
            characterized_pump["final_head"] =  characterized_pump["pressure"][index]
            characterized_pump["final_efficiency"] =  characterized_pump["pump_efficiency"][index]

        self.progressBar.setValue(20)

        # Generate the graphs of power, pressure, efficiency vs flow
        if characterized_pump["pump_type"] == "roto":
            degree = 3
        elif characterized_pump["pump_type"] == "triplex":
            degree = 1

        print(characterized_pump)

        if not testing_interface:
            flow_vs_pump_power = Plotter(characterized_pump["flow"], characterized_pump["pump_power"],"Flujo vs Potencia","Flujo (L/min)","Potencia (W)", "FlowVsPower.png", 3)
            flow_vs_pump_power.plotter()

        self.progressBar.setValue(30)

        if not testing_interface:
            flow_vs_pressure = Plotter(characterized_pump["flow"], characterized_pump["pump_total"],"Flujo vs Cabeza","Flujo (L/min)","Cabeza (m)", "FlowVsHead.png", degree)
            flow_vs_pressure.plotter()
        
        
        if not testing_interface:
            flow_vs_pump_efficiency = Plotter(characterized_pump["flow"], characterized_pump["pump_efficiency"],"Flujo vs Eficiencia" ,"Flujo (L/min)","Eficiencia (%)", "FlowVsEfficiency.png", 3)
            flow_vs_pump_efficiency.plotter()


        # f = open('example.txt', 'w')

        # hydraulic_power_curve = 998.8 * 9.798 *  head_curve * flow_curve * (1 / 60000) 

        # efficiency_curve = hydraulic_power_curve / power_curve

        # with open('readme.txt', 'w') as f:
        #     f.write(hydraulic_power_curve)
        #     f


        # flow_vs_pump_efficiency.plotInterpolatedCurves(flow_curve, efficiency_curve)
        self.progressBar.setValue(40)

        

        # Generate a html file that is going to be used as a base for the pdf generation
        # if not testing_interface:
        generate_html(characterized_pump)
        
        self.progressBar.setValue(50)
 
        # resd to sample.json
        with open(directory_path + "/data/json/test_count.json", "r") as openfile:
            json_object = json.load(openfile)

        # Generate the final report in pdf
            
        characterized_pump['test_number'] = json_object["test_number"] + 1
        
        generate_pdf(characterized_pump['test_number'], characterized_pump["service_order"])

        self.progressBar.setValue(70)
        
        # Send report
        send_email(characterized_pump['test_number'], characterized_pump["service_order"], characterized_pump['date'], 
                    characterized_pump["delegate"], characterized_pump['model'], characterized_pump["parking_slot"])

        # Update the report counter
        
        json_object = json.dumps({"test_number" : characterized_pump['test_number']}, indent=4)
 
        # Writing to sample.json
        with open(directory_path + "/data/json/test_count.json", "w") as outfile:
            outfile.write(json_object)

        

            
        self.progressBar.setValue(100)

        self.alerts.setText("Generación de reporte finalizado")

        self.pushButton.setEnabled(True)

        self.pushButton.setText("Caracterizar otra bomba")

first_flank_detected_time = 0
second_flank_detected_time = 0
first_flank_detected = False
second_flank_detected = False


""" def next(widget, button_pin):

    # previous_state = GPIO.input(button_pin)
    global first_flank_detected_time
    global second_flank_detected_time
    global first_flank_detected

    

    if first_flank_detected:
        second_flank_detected_time = time.time() - first_flank_detected_time
        print(second_flank_detected_time)
        if second_flank_detected_time >= 0.3 and second_flank_detected_time <= 2:
            print("Green button pressed.")
            QTimer.singleShot(200, widget.currentWidget().goToNextTask)

        first_flank_detected = False
        # second_flank_detected = True

    else:
        first_flank_detected_time = time.time()
        first_flank_detected = True
        # second_flank_detected = False

    # if second_flank_detected_time >= 0.3 and second_flank_detected_time <= 1.5 and second_flank_detected:
    #     print("Green button pressed.")
    #     widget.currentWidget().goToNextTask()




    # while True:
    #     current_state = GPIO.input(button_pin)
    #     #print(f"pin {4}: {str(GPIO.input(4))}")
    #     if current_state != previous_state:
    #         # Flank detected
    #         second_flank_detected_time = time.time()
        
    #     if second_flank_detected_time - first_flank_detected_time >= 0.5:
    #         # Signal has stayed in the new state for at least 1 second
    #         print("Green button pressed.")
    #         widget.currentWidget().goToNextTask()
    #         break

    #     elif time.time() - first_flank_detected_time >= 3:
    #         return
        
    #     previous_state = current_state
        
    #     # Add a small delay to avoid high CPU usage
    #     time.sleep(0.01)



    

    # widget.widget(widget_index).goToNextTask() """


def closeApp(widget, button_pin):

    previous_state = GPIO.input(button_pin)
    first_flank_detected_time = time.time()
    second_flank_detected_time = 0

    while True:
        current_state = GPIO.input(button_pin)
        #print(f"pin {4}: {str(GPIO.input(4))}")
        if current_state != previous_state:
            # Flank detected
            second_flank_detected_time = time.time()
        
        if second_flank_detected_time - first_flank_detected_time >= 1:
            # Signal has stayed in the new state for at least 1 second
            print("Red button pressed.")
            break

        elif time.time() - first_flank_detected_time >= 3:
            return
        
        previous_state = current_state
        
        # Add a small delay to avoid high CPU usage
        time.sleep(0.01)



    widget.close()
    os.system("shutdown -h +1") 

def turnOnLed(led_pin):

    GPIO.output(led_pin,GPIO.HIGH)

 
        



if __name__ == '__main__':

   
    # ser = serial.Serial('/dev/ttyACM0', 115200, timeout=0)
    # ser.reset_input_buffer()

    app = QtWidgets.QApplication(sys.argv)

    screen = app.primaryScreen()
    screen_width = screen.availableGeometry().width()
    screen_height = screen.availableGeometry().height()

       
    

    # Button pin definitions    ******************************************************************************
    if not testing_interface or testing_buttons:
        GPIO.setmode(GPIO.BCM)
        

        synthetic_gnd_pin = 23
        GPIO.setup( synthetic_gnd_pin , GPIO.OUT)
        
        GPIO.output( synthetic_gnd_pin, GPIO.HIGH)
        time.sleep(1)
        GPIO.output( synthetic_gnd_pin, GPIO.LOW)

        red_button_pin = 22 # Button to close the app
        GPIO.setup(red_button_pin, GPIO.IN)
        print(str(GPIO.input(red_button_pin)))
        GPIO.add_event_detect(red_button_pin, GPIO.FALLING, callback = lambda x: closeApp(widget, red_button_pin), bouncetime = 300)

        """ green_button_pin = 27 # Button to advance though the user interface
        GPIO.setup(green_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        print(str(GPIO.input(green_button_pin)))
        GPIO.add_event_detect(green_button_pin, GPIO.RISING, callback = lambda x: next(widget, green_button_pin), bouncetime = 300) """
        # GPIO.add_event_detect(green_button_pin, GPIO.FALLING, callback = lambda x: closeApp(widget))

        green_led_pin = 0 #! Define pins
        GPIO.setup(green_led_pin,GPIO.OUT)

        red_led_pin = 0
        GPIO.setup(red_led_pin,GPIO.OUT)

    widget = QtWidgets.QStackedWidget()

    information_window = FirstWindow(directory_path + "/Information_screen.ui", screen_width)
    widget.addWidget(information_window)

    measurements_window = SecondWindow(directory_path + "/Measurements_screen.ui", screen_width)
    widget.addWidget(measurements_window)

    resume_window = ThirdWindow(directory_path + '/Resume_screen.ui', screen_width)
    widget.addWidget(resume_window)

    report_generation_window = FourthWindow(directory_path + "/Generate_Report.ui", screen_width)
    widget.addWidget(report_generation_window)

    button_window = PyQt_RPI(widget)
    # widget.addWidget(button_window)

    # widget.setFixedWidth(screen_width)
    # widget.setFixedHeight(screen_height)
    widget.showFullScreen()
    widget.show()



    sys.exit(app.exec_())

