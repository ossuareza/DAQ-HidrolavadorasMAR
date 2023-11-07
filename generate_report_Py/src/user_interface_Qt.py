import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi
from PyQt5.QtGui import QFont

title = QFont("Ubuntu", 20)

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
                if "label" in element.widget().objectName():
                    element.widget().setStyleSheet(f''' font-size: {text_font_size}px; ''')

                if "title" in element.widget().objectName():
                    element.widget().setStyleSheet(f''' font-size: {title_font_size}px; ''')
                
                if "Button" in element.widget().objectName():
                    element.widget().setStyleSheet(f''' font-size: {button_font_size}px; ''')
                
                if "alerts" in element.widget().objectName():
                    element.widget().setStyleSheet(f''' font-size: {int(title_font_size* 3/2)}px; color: green''')
                    # element.widget().setStyleSheet("color: green")
            self.defineFontSizes(element)



class FirstWindow(Window):
    def __init__(self, path, screen_width):
        super().__init__(path, screen_width)
        self.pushButton.clicked.connect(self.goToNextScreen)

        # self.order_service
        # self.delegate
        # self.date
        # self.pump_model
        # self.measurements
    
    def goToNextScreen(self):
        widget.setCurrentIndex(1)

        # self.order_service = self.order_service.text()
        # self.delegate = self.delegate.text()
        # self.date = self.date.text()
        # self.pump_model = self.pump_model.text()
        # self.measurements = self.measurements.text()

class SecondWindow(Window):
    def __init__(self, path, screen_width):
        super().__init__(path, screen_width)
        self.pushButton.clicked.connect(self.goToNextScreen)
    
    def goToNextScreen(self):
        widget.setCurrentIndex(0)
        



characterized_pump = {
    "motor_speed" : 0, 
    "power" : 0, 
    "parking_slot" : 0,
    "test_number" : 0,
    "service_order" : "", 
    "date" : "", 
    "delegate" : "", 
    "model" : "",
    "flow" : [], 
    "pressure" : [], 
    "velocity" : [], 
    "elevation" : [], 
    "pump_total" : [], 
    "pump_power" : [], 
    "pump_efficiency" : [],
    "final_flow" : 0,
    "final_head" : 0, 
    "final_efficiency" : 0
}


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
sys.exit(app.exec_())