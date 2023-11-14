import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QTimer, QThread, QObject, pyqtSignal
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap, QImage

from six.moves.queue import Queue
# from threading import *

from generate_html import generate_html
from generate_pdf import generate_pdf
from plotter import plotter

# import serial
# import modbus_tk.defines as cst
# from modbus_tk import modbus_rtu

import time
# !import Adafruit_ADS1x15
# !import RPi.GPIO as GPIO

import numpy as np
import pandas as pd

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


water_density_df = pd.read_excel("data/density/Densidad_agua.xlsx") # Load table for water densities at different temperatures



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
                if "logo" in element.widget().objectName():
                    pixmap_image = QPixmap("data/imgs/logo.png")
                    element.widget().setPixmap(pixmap_image.scaledToWidth(self.screen_width // 6))
                    element.widget().setAlignment(Qt.AlignCenter)
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
        characterized_pump["total_measurements"] = int(self.measurements.text())

class SecondWindow(Window):
    def __init__(self, path, screen_width):
        super().__init__(path, screen_width)

        self.alerts.setText("Preparado para empezar con la rutina de medición")
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

        # self.pressure_in = 0
        # self.pressure_out = 0
        # self.power = 0
        # self.temperature = 0

        self.actual_step = 0
        self.progressBar.setMaximum(100)
        self.progressBar.setValue(0)

        self.different_apertures = []

        self.timer = QTimer(self)
        self.timer_flow_measurement = QTimer(self)

        self.timer.timeout.connect(self.defineButtonState)
        self.timer.timeout.connect(self.takeSensorsData)
        
        self.timer.start(1000)

        self.contador_random = 0


    def takeSensorsData(self):

        # Display sensors data on screen
        self.lcdNumber_f.display(self.contador_random) #! Modify with the pump dictionary
        self.lcdNumber_pin.display(self.contador_random)
        self.lcdNumber_pout.display(self.contador_random)
        self.lcdNumber_pw.display(self.contador_random)
        self.lcdNumber_t.display(self.contador_random)
        
    def defineButtonState(self):
        # Disable pushButton while a requirement is not achieved
        if len(self.different_apertures) > 0 and len(self.different_apertures) > self.actual_step // 2:
            if self.flow >= self.different_apertures[self.actual_step // 2]:
                self.pushButton.setEnabled(True)

        self.contador_random += 1

    def goToNextTask(self):
        print(f"actual_step: {self.actual_step // 2}")

        # If all the measurements were taken, then go to next screen
        if self.actual_step // 2 == characterized_pump["total_measurements"]:
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
                
            self.alerts.setText("Midiendo caudal máximo")
            self.alerts.setStyleSheet(f''' color: green ''')
            # Whe the valve is completely open, take tha measured flow as the maximum flow
            self.max_flow = self.flow

            # Define the apertures for each measurement point
            self.different_apertures = self.max_flow * np.linspace(1, 0.4, characterized_pump["total_measurements"])

            self.actual_step += 1

        elif self.actual_step % 2 == 0:
            # Show in screen the target flow
            self.label_fo.show()
            self.lcdNumber_fo.show()
            self.label_fo_units.show()
            
            # Define target flow
            target_flow = self.different_apertures[self.actual_step // 2]

            # Show alerts to guide the search process of the target flow
            self.alerts.setText(f"Cierre la válvula hasta flujo de {target_flow } L/min")
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

            self.worker_on_thread = workerOnThread()
            self.worker_on_thread.moveToThread(self.thread1)

            self.thread1.started.connect(self.worker_on_thread.check)
            self.worker_on_thread.finished.connect(self.thread1.quit)
            self.worker_on_thread.finished.connect(self.worker_on_thread.deleteLater)
            self.thread1.finished.connect(self.thread1.deleteLater)
            self.worker_on_thread.progress.connect(self.reportProgress)
            self.worker_on_thread.flag.connect(self.checkFinished)
                    
            self.thread1.start() 

            self.thread1.finished.connect(
                lambda: self.pushButton.setEnabled(True)
            )

            # self.takeMeasurement()

            
    def reportProgress(self, n):
        self.alerts.setText(f"Time: {n}")

    def checkFinished(self, check_flag):
        if check_flag:
            self.alerts.setText("Se ha hallado la estabilidad")
            self.alerts.setStyleSheet(f''' color: green ''')
            self.pushButton.setEnabled(True)
            
            bar_value = int((self.actual_step // 2 + 1) / characterized_pump["total_measurements"] * 100)
            self.lcd_measurement.display(self.actual_step // 2 + 1)
            self.progressBar.setValue(bar_value)
            self.progressBar.setFormat("%.02f %%" % bar_value)


            # self.worker_on_thread.moveToThread(self.thread1)

            # self.thread2 = QThread()

            self.worker_on_thread = workerOnThread()
            self.worker_on_thread.moveToThread(self.thread1)

            self.thread1.started.connect(self.worker_on_thread.measurementsAverage)
            self.worker_on_thread.finished.connect(self.thread1.quit)
            self.worker_on_thread.finished.connect(self.worker_on_thread.deleteLater)
            self.thread1.finished.connect(self.thread1.deleteLater)
            self.worker_on_thread.measurements_ready.connect(self.takeMeasurement)
            # self.worker_on_thread.flag.connect(self.measurementsAverageFinished)

            self.actual_step += 1
        else:
            self.alerts.setText("No se ha podido hallar estabilidad")
            self.alerts.setStyleSheet(f''' color: red ''')

    # def measurementsAverageFinished(self):

    
    def takeMeasurement(self, measurements): #! Run it in a thread ---------------------------------------------------------------
        # measurements_counter = 0
        # start_time = time.time()

        pressure_in = measurements[0]
        pressure_out = measurements[1]
        electrical_power = measurements[2]
        temperature = measurements[3]
        
        

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
        
        water_density = float(water_density_df[water_density_df['Temperatura °C'] == temperature]['Densidad kg / m3'].iloc[0])
        g = 9.79

        if characterized_pump["pump_type"] == "roto":            
            z1 = 0.851
            z2 = 1.637
            tube_area = ((51,8 * 10 ** (-3)) / 4) ** 2 * np.pi # m^2

        elif characterized_pump["pump_type"] == "triplex": 
            z1 = 0.435
            z2 = 0.603
            tube_area = ((24,8 * 10 ** (-3)) / 4) ** 2 * np.pi # m^2
        else:
            z1 = 0
            z2 = 0
            tube_area = 1

        
        flow_velocity = self.flow / tube_area / 60000 # m/s
        losts_1 = 0 #! Waiting for the calculations
        losts_2 = 0
        velocity_head_1 = z1 + pressure_in  / (water_density * g) + (flow_velocity)**2 / (2*g) + losts_1
        velocity_head_2 = z2 + pressure_out / (water_density * g) + (flow_velocity)**2 / (2*g) + losts_2

        pump_total = velocity_head_2 - velocity_head_1

        characterized_pump["flow"].append(self.flow)
        characterized_pump["pressure"].append(pressure_out)
        characterized_pump["velocity"].append(velocity_head_2)
        characterized_pump["elevation"].append(z2 - z1)
        characterized_pump["pump_total"].append(pump_total)
        characterized_pump["pump_power"].append(electrical_power)

        hydraulic_power = pressure_out * self.flow / 60 #! Correct equation
        characterized_pump["pump_efficiency"].append(hydraulic_power / electrical_power * 100)
        


    def measurePower(self):

        try:
            # Connect to the slave
            serial = serial.Serial(
                                port='/dev/ttyUSB0',  #! Modify depending on the connection
                                baudrate=9600,
                                bytesize=8,
                                parity='N',
                                stopbits=1,
                                xonxoff=0
                                )
            master = modbus_rtu.RtuMaster(serial)
            master.set_timeout(2.0)
            master.set_verbose(True)

            data = master.execute(1, cst.READ_INPUT_REGISTERS, 0, 10)

            power = (data[3] + (data[4] << 16)) / 10.0
        
        except Exception as e:
            print(e)
        finally:
            master.close()
            return power

    def measureTemperature(self):
        pass

    def countingFlowPulses(self, channel):

        self.flow_measurement_time = 10 # sec
        if not self.flow_measurement_started:
            self.flow_measurement_started = True
            self.start_time_flow_measurement = time.time()
            self.flowmeter_pulses += 1

            self.timer_flow_measurement.timeout.connect(self.definingFlow)
            self.timer.start(self.flow_measurement_time * 1000)
        else:
            self.flowmeter_pulses += 1
    
    def definingFlow(self):
        
        if time.time() - self.start_time_flow_measurement >= self.flow_measurement_time:
            self.flow = self.flowmeter_pulses * 6
            self.flow_measurement_started = False
            self.flowmeter_pulses = 0
            


            
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
            widget.setCurrentIndex(0)
            return

        self.alerts.setText("Generando reporte")

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

        self.progressBar.setValue(20)

        # Generate the graphs of power, pressure, efficiency vs flow
        plotter(characterized_pump["flow"], characterized_pump["pump_power"], "FlowVsPower.png","Flujo vs Potencia","Flujo (L/min)","Potencia (kW)")
        self.progressBar.setValue(30)
        plotter(characterized_pump["flow"], characterized_pump["pressure"], "FlowVsHead.png","Flujo vs Cabeza","Flujo (L/min)","Cabeza (m)")
        self.progressBar.setValue(40)
        plotter(characterized_pump["flow"], characterized_pump["pump_efficiency"], "FlowVsEfficiency.png","Flujo vs Eficiencia","Flujo (L/min)","Eficiencia (%)")
        self.progressBar.setValue(50)

        # Generate a html file that is going to be used as a base for the pdf generation
        generate_html(characterized_pump)
        self.progressBar.setValue(70)

        # Generate the final report in pdf
        generate_pdf(characterized_pump["test_number"])
        self.progressBar.setValue(100)

        self.alerts.setText("Generación de reporte finalizado")


        
 #! Una idea para poder lidiar con las interrupciones de GPIO en caso de que hayan problemas       
class GpioThread(QThread):
    event_detected = pyqtSignal(int)
    def __init__(self, *args, **kwargs):
        QThread.__init__(self, *args, **kwargs)
        self.queue = Queue()
        GPIO.add_event_detect(channel, GPIO.BOTH, callback=self.queue.put)

    def run(self):
        while True:
            self.event_detected.emit(self.queue.get())




class workerOnThread(QObject):

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
    
    measurements_ready = pyqtSignal(list)

    def measurementsAverage(self):
        
        measurements_counter = 0
        start_time = time.time()

        pressure_in = 0
        pressure_out = 0
        electrical_power = 1
        temperature = 0

        while time.time() - start_time < 2:
            pressure_in += 0 # adc.read_adc(sensor_1_pin, gain=gain) * (4.096/32767) #! * 14.503773773 to psi
            pressure_out += 0 # adc.read_adc(sensor_2_pin, gain=gain) * (4.096/32767) #! * 14.503773773 to psi
            # electrical_power += self.measurePower()
            # temperature += self.measureTemperature()

            measurements_counter += 1
        
        pressure_in /= measurements_counter
        pressure_out /= measurements_counter
        electrical_power /= measurements_counter
        temperature /= measurements_counter
        self.measurements_ready.emit([pressure_in, pressure_out, electrical_power, temperature])
        self.finished.emit()

if __name__ == '__main__':

    #! GPIO.setmode(GPIO.BCM)

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

    if characterized_pump["pump_type"] == "roto":
        flowmeter_pin = 4 #! Definir bien los pines
    elif characterized_pump["pump_type"] == "triplex":
        flowmeter_pin = 17
    
    # GPIO.setup(flowmeter_pin, GPIO.IN)
    
    # GPIO.add_event_detect(flowmeter_pin, GPIO.RISING, callback=measurements_window.countingFlowPulses)

    report_generation_window = ThirdWindow("Generate_Report.ui", screen_width)
    widget.addWidget(report_generation_window)

    widget.show()

    # if stopButton.is_pressed: #Check to see if button is pressed
    #         time.sleep(1) # wait for the hold time we want. 
    #         if stopButton.is_pressed: #check if the user let go of the button
    #             os.system("shutdown now -h") #shut down the Pi -h is or -r will reset


    sys.exit(app.exec_())

