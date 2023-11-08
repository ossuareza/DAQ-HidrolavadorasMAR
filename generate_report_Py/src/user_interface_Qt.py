import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QTimer
from PyQt5.uic import loadUi
from PyQt5.QtGui import QFont

from generate_html import generate_html
from generate_pdf import generate_pdf
from plotter import plotter

import time
# !import Adafruit_ADS1x15
# !import RPi.GPIO as GPIO

import numpy as np


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

# !adc = Adafruit_ADS1x15.ADS1115()

class Window(QtWidgets.QMainWindow):
    def __init__(self, path, screen_width):
        super(Window,self).__init__()
        loadUi(path,self)
        self.screen_width = screen_width

        self.defineFontSizes(self.centralwidget)
        
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
            self.defineFontSizes(element)



class FirstWindow(Window):
    def __init__(self, path, screen_width):
        super().__init__(path, screen_width)
        self.pushButton.clicked.connect(self.goToNextTask)
    
    def goToNextTask(self):
        widget.setCurrentIndex(1)

        if self.roto.isChecked():
            characterized_pump["pump_type"] = "roto"
        if self.triplex.isChecked():
            characterized_pump["pump_type"] = "triplex" 

        characterized_pump["service_order"] = self.lE_1_service_order.text()
        characterized_pump["delegate"] = self.lE_2_delegate.text()
        characterized_pump["date"] = self.lE_3_date.text()
        characterized_pump["pump_model"] = self.lE_4_pump_model.text()
        characterized_pump["total_measurements"] = self.measurements.text()

        

        

        print(characterized_pump)

class SecondWindow(Window):
    def __init__(self, path, screen_width):
        super().__init__(path, screen_width)

        self.alerts.setText("Abra la válvula completamente")
        self.alerts.setStyleSheet(f''' color: green ''')

        self.pushButton.clicked.connect(self.goToNextTask)
        # !GPIO.setmode(GPIO.BCM)

        if characterized_pump["pump_type"] == "roto":
            flowmeter_pin = 7 #! Definir bien los pines
        elif characterized_pump["pump_type"] == "triplex":
            flowmeter_pin = 7


        # !GPIO.setup(flowmeter_pin, GPIO.IN)
        self.flowmeter_pulses = 0
        # !GPIO.add_event_detect(flowmeter_pin, GPIO.RISING, callback=self.measuringFlow())
        self.actual_flow = 0
        self.flow_measurement_started = False
        self.start_time_flow_measurement = 0
        self.flow = 0
        self.pulses_per_liter = 0 #! Define conversion factor

        self.max_flow = 0

        self.actual_measurement = 0

        self.different_apertures = 0

    def goToNextTask(self):
        
        #! En la primera medición se debe tener la válvula completamente abierta

        if self.actual_measurement == 0:

            self.max_flow = self.flow

            #! Definir caudales deseados a partir del caudal de la válvula totalmente abierta

            self.different_apertures = self.max_flow * np.linspace(1, 0.4, characterized_pump["total_measurements"])

        if self.actual_measurement % 2 == 0:
            self.alerts.setText("Abra la válvula completamente")
            while self.flow <= self.different_apertures[self.actual_measurement // 2]:
                self.pushButton.setEnable(False)
            
            self.pushButton.setDisabled(False)

        #! Después se debe hacer el sistema que espera a que se alcance el flujo esperado e intercambiar las señales de alerta

        elif self.actual_measurement % 2 == 1:

            if not self.checkStability(): #! Define function
                pass

            self.takeMeasurement(self.actual_measurement)
                
            self.actual_measurement += 1

        if self.actual_measurement // 2 == characterized_pump["total_measurements"]:
            widget.setCurrentIndex(2)
            

    def takeMeasurement(self, counter):
        pass

    def checkStability(self):

        self.alerts.setText("Midiendo estabilidad del sistema")
        self.alerts.setStyleSheet(f''' color: green ''')

        gain = 1
        if characterized_pump["pump_type"] == "roto": #!Change pin numbers            
            sensor_1_pin = 0
            sensor_2_pin = 0

        if characterized_pump["pump_type"] == "roto": #!Change pin numbers
            sensor_1_pin = 0
            sensor_2_pin = 0

        average_m_1 = 0
        average_m_2 = 0
        data_counter = 0
        start_count_stabilization_time = time.time()
        start_checking_process_time = time.time()

        while True:
            
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
                    self.alerts.setText("No se ha podido hallar estabilidad")
                    self.alerts.setStyleSheet(f''' color: red ''')
                    return False
            
            if time.time() - start_count_stabilization_time >= 10:
                self.alerts.setText("Se ha hallado la estabilidad")
                self.alerts.setStyleSheet(f''' color: green ''')
                return True
            
    def measuringFlow(self):
        if not self.flow_measurement_started:
            self.flow_measurement_started = True
            self.start_time_flow_measurement = time.time()
            self.flowmeter_pulses += 1
        else:
            self.flowmeter_pulses += 1
        
        if time.time() - self.start_time_flow_measurement >= 1:
            self.flow = self.flowmeter_pulses / self.pulses_per_liter * 60
            self.flow_measurement_started = False
            


            
class ThirdWindow(Window):
    def __init__(self, path, screen_width):
        super().__init__(path, screen_width)
        self.pushButton.clicked.connect(self.goToNextTask)
    
    def goToNextTask(self):

        characterized_pump["flow"] = [1,2,3,4,5,6,7,8,9,10]
        characterized_pump["pressure"] =  [55, 54.5, 54, 53, 52.5, 51.7, 50, 48.5, 46, 44]
        characterized_pump["velocity"] =  [1,2,3,4,5,6,7,8,9,10]
        characterized_pump["elevation"] =  [1,2,3,4,5,6,7,8,9,10]
        characterized_pump["pump_total"] =  [1,2,3,4,5,6,7,8,9,10]
        characterized_pump["pump_power"] =  [6,12,14,20,22,24,35,45,44,53]
        characterized_pump["pump_efficiency"] =  [0,10,20,20,25,30,40,70,60,50]

        # Finding most efficient point
        index = characterized_pump["pump_efficiency"].index(max(characterized_pump["pump_efficiency"])) 
        characterized_pump["final_flow"] =  characterized_pump["flow"][index]
        characterized_pump["final_head"] =  characterized_pump["pressure"][index]
        characterized_pump["final_efficiency"] =  characterized_pump["pump_efficiency"][index]

        # Generate the graphs of power, pressure, efficiency vs flow
        plotter(characterized_pump["flow"], characterized_pump["pump_power"], "FlowVsPower.png","Flujo vs Potencia","Flujo (L/min)","Potencia (kW)")
        plotter(characterized_pump["flow"], characterized_pump["pressure"], "FlowVsHead.png","Flujo vs Cabeza","Flujo (L/min)","Cabeza (m)")
        plotter(characterized_pump["flow"], characterized_pump["pump_efficiency"], "FlowVsEfficiency.png","Flujo vs Eficiencia","Flujo (L/min)","Eficiencia (%)")

        # Generate a html file that is going to be used as a base for the pdf generation
        generate_html(characterized_pump)

        # Generate the final report in pdf
        generate_pdf(characterized_pump["test_number"])
        
        






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


# widget.setFixedWidth(screen.availableGeometry().width())
# widget.setFixedHeight(screen.availableGeometry().height())




widget.show()

# while True:
#     if widget.currentIndex() == 2:
#         measurements_window.pushButton.setEnable(False)
#         QTimer.singleShot(5000, lambda: measurements_window.pushButton.setDisabled(False))
#         break

sys.exit(app.exec_())

