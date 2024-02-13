import matplotlib.pyplot as plt
from generate_html import generate_html
from generate_pdf import generate_pdf
from plotter import Plotter
import numpy as np
import os
import sys

characterized_pump = {
    "motor_speed" : 3450, 
    "power" : 750, 
    "parking_slot" : 1,
    "test_number" : 5,
    "service_order" : "23-0814", 
    "date" : "23/11/2023", 
    "delegate" : "Felipe Rodriguez", 
    "model" : "CPM620",
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

    "temperature": 0
}


characterized_pump["flow"] =        [80.5, 71.9, 65.0, 55.8, 50.0, 45.3, 34.8, 35.2]
characterized_pump["pressure"] =    [2.12, 31.47, 39.0, 45.5, 49.3, 54.3, 56.4, 56.2]
characterized_pump["velocity"] =    [0.045, 0.036, 0.029, 0.022, 0.017, 0.014, 0.008, 0.009]
characterized_pump["elevation"] =   [0.655, 0.655, 0.655, 0.655, 0.655, 0.655, 0.655, 0.655]
characterized_pump["pump_total"] =  [4.5, 24.7, 29.6, 33.7, 36.0, 39.2, 40.6, 40.3]
characterized_pump["pump_power"] =  [672.46, 693.78, 677.58, 651.1, 627.8, 592.3, 575.7, 574.2]
characterized_pump["pump_efficiency"] =  [8.9, 41.8, 46.3, 47.2, 46.9, 49.0, 40.0, 40.4]

characterized_pump["flow"] =             [80.2, 68.9, 57.9, 46.9, 35.5]
characterized_pump["pressure"] =         [3.12, 23.2, 28.4, 32.4, 35.8]
characterized_pump["velocity"] =         [0.045, 0.033, 0.023, 0.015, 0.009]
characterized_pump["elevation"] =        [0.655, 0.655, 0.655, 0.655, 0.655]
characterized_pump["pump_total"] =       [8.1, 21.6, 24.7, 27.1, 29.0]
characterized_pump["pump_power"] =       [659.9, 675.2, 644.9, 605.8, 566.9]
characterized_pump["pump_efficiency"] =  [16.1, 36.0, 36.2, 34.2, 29.6]

# Finding most efficient point
index = characterized_pump["pump_efficiency"].index(max(characterized_pump["pump_efficiency"])) 
characterized_pump["final_flow"] =  characterized_pump["flow"][index]
characterized_pump["final_head"] =  characterized_pump["pressure"][index]
characterized_pump["final_efficiency"] =  characterized_pump["pump_efficiency"][index]

def generate_report(characterized_pump):

    script_path = os.path.abspath(sys.argv[0])
    src_path = os.path.dirname(script_path)
    directory_path = os.path.dirname(src_path)

    # Generate the graphs of power, pressure, efficiency vs flow
    # plotter(characterized_pump["flow"], characterized_pump["pump_power"], "FlowVsPower.png","Flujo vs Potencia","Flujo (L/min)","Potencia (W)")
    # plotter(characterized_pump["flow"], characterized_pump["pressure"], "FlowVsHead.png","Flujo vs Cabeza","Flujo (L/min)","Cabeza (m)")
    # plotter(characterized_pump["flow"], characterized_pump["pump_efficiency"], "FlowVsEfficiency.png","Flujo vs Eficiencia","Flujo (L/min)","Eficiencia (%)")

    flow_vs_pump_power = Plotter(characterized_pump["flow"], characterized_pump["pump_power"],"Flujo vs Potencia","Flujo (L/min)","Potencia (W)", "FlowVsPower.png")
    flow_vs_pump_power.plotter()
    # self.progressBar.setValue(30)


    flow_vs_pressure = Plotter(characterized_pump["flow"], characterized_pump["pump_total"],"Flujo vs Cabeza","Flujo (L/min)","Cabeza (m)", "FlowVsHead.png")
    flow_vs_pressure.plotter()
    # self.progressBar.setValue(40)
    
    flow_vs_pump_efficiency = Plotter(characterized_pump["flow"], characterized_pump["pump_efficiency"],"Flujo vs Eficiencia" ,"Flujo (L/min)","Eficiencia (%)", "FlowVsEfficiency.png")
    flow_vs_pump_efficiency.plotter()

    # Generate a html file that is going to be used as a base for the pdf generation
    generate_html(characterized_pump)

    # Generate the final report in pdf
    generate_pdf(characterized_pump["test_number"])

# generate_report(characterized_pump)


manometer_pressure = np.array([0, 26, 33.5, 39, 40])#/14.503773773
manometer_flow =     np.array([78.56, 64.2, 50.7, 36.5, 35.5])


manometer_plotter = Plotter(manometer_flow[1:], manometer_pressure[1:], "Flujo vs Potencia","Flujo (L/min)","Potencia (W)", "FlowVsPower.png")

coefficients_manometer = manometer_plotter.optimization()
curve = np.poly1d(coefficients_manometer)

manometer_x_curve = np.linspace(0, max(manometer_flow), 100)
manometer_y_curve = curve(manometer_x_curve)

sensor_flow =        np.array([80.2, 68.9, 57.9, 46.9, 35.5])
sensor_pressure =    np.array([3.12, 23.2, 28.4, 32.4, 35.8])#/14.503773773

sensor_plotter = Plotter(sensor_flow[1:], sensor_pressure[1:], "Flujo vs Potencia","Flujo (L/min)","Potencia (W)", "FlowVsPower.png")

coefficients_sensor = sensor_plotter.optimization()
curve = np.poly1d(coefficients_sensor)

sensor_x_curve = np.linspace(0, max(sensor_flow), 100)
sensor_y_curve = curve(manometer_x_curve)


plt.figure(figsize=(15,5))
plt.grid(color='0.7', linestyle='--')
plt.scatter(manometer_flow, manometer_pressure, color='black', zorder=2)
plt.plot(manometer_x_curve, manometer_y_curve, zorder=1)
plt.scatter(sensor_flow, sensor_pressure, color='red', zorder=2)
plt.plot(manometer_x_curve, sensor_y_curve, zorder=1)

print(max(abs(sensor_y_curve - manometer_y_curve)))

print(max(sensor_y_curve) * 0.06)


plt.title("Manómetro vs Sensor digital")
plt.xlabel("Flujo (L/min)")
plt.ylabel("Presión (psi)")
plt.legend(['Manómetro','','Sensor digital',''])
path_to_img = os.path.join(directory_path, "data", "imgs", "Comparación de sensores")
# plt.show()
plt.savefig(path_to_img)
