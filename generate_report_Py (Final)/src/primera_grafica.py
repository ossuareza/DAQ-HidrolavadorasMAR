
from plotter import Plotter
import pandas as pd
import numpy as np

from scipy.interpolate import CubicSpline
# import matplotlib
# # matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os

from scipy.optimize import minimize

# Example data

flow = np.array([105.20055380540562, 75.25551423341244, 103.26986879636785, 60.43984307049808, 57.77514987700942])
pressure_out = np.array([0.0, 30.426575092318497, 38.82317180486466, 44.602205979491565, 0.0])
velocity = np.array([0.04457904675219594, 0.037967854645320126, 0.03269014126651821, 0.026516623180021, 0.024100355261270856])
elevation = np.array([0.655, 0.655, 0.655, 0.655, 0.655])
pump_total = np.array([1.868426657638853, 24.060700214429072, 29.68524678026441, 33.364485958493226, 1.311046182831139])

pump_total2 = [ 2.33306626, 23.70867088, 29.51269453, 33.45189834,  1.95647363]




flow = np.array([80.5778618732867, 72.46017340348098, 64.81229644608973, 55.50125709043111, 47.99218724597655, 40.85957349944416, 36.160751946585286, 45.08251496125297])
pump_total = np.array([4.743741781233289, 23.93457712913942, 29.624942516692194, 33.832237857372185, 36.6913770151439, 39.112487738327786, 40.350729308921935, 40.576362603665])


x_data = flow
y_data = pump_total


class Plotter():

    def __init__(self, x_data, y_data, title, x_label, y_label, file_name):
        self.x_data = x_data
        self.y_data = y_data
        self.title = title
        self.x_label = x_label
        self.y_label = y_label
        self.file_name = file_name

    # Curve model (polynomial of degree 2)
    def curve_model(self, x, params):
        return params[0] * x**3 + params[1] * x**2 + params[2] * x + params[3]

    # Objective function
    def objective(self, params):
        return sum((self.curve_model(x, params) - y)**2 for x, y in zip(self.x_data, self.y_data))

    # Constraint function
    def constraint(self, params):
        # Derivative at the maximum point should be 0
        x_max = - params[1] / (3 * params[0])
        return x_max
    
    def constraint_2nd_derivative(self, params):
         return np.logical_xor(6 * params[0] < 0, True)


    def optimization(self):

        # Optimization with constraint
        result = minimize(self.objective, x0=[1, 1, 1, 1], constraints=[{'type': 'eq', 'fun': self.constraint}, {'type': 'ineq', 'fun': self.constraint_2nd_derivative}])

        # Extract optimized parameters
        return result.x

    def plotter(self):

        coefficients = self.optimization()
        curve = np.poly1d(coefficients)

        # Generate more points on the curve for a smoother plot
        x_curve = np.linspace(0, max(self.x_data), 100)
        y_curve = curve(x_curve)
    
        # Plot the interpolated curve
        plt.figure(figsize=(15,5))
        plt.grid(color='0.7', linestyle='--')
        plt.plot(x_curve, y_curve, zorder=1)
        plt.scatter(self.x_data, self.y_data, color='black', zorder=2)
        plt.scatter(x_curve[np.where(y_curve == y_curve.max())][0], y_curve.max(), color='red', zorder=3)
        plt.title(self.title)
        plt.xlabel(self.x_label)
        plt.ylabel(self.y_label)
        path_to_img = os.path.join("data", "imgs", self.file_name)
        # plt.show()
        plt.savefig(path_to_img)


flow_vs_pressure = Plotter(flow, pump_total,"Flujo vs Cabeza","Flujo (L/min)","Cabeza (m)", "Prueba_3.png")
flow_vs_pressure.plotter()


# def haalandCalculations(e, D, water_viscosity, V):
#     Re = (D * V) / (water_viscosity)
#     f_raiz = (-1.8 * np.log((( e / D) / 3.7) ** 1.11 + (6.9 / (Re + 0.000001)))) ** (-1) #! Delete the epsilon
#     return f_raiz ** 2





# e_mang_trans = 0.0020 * 10 ** (-3) # m
# e_mang_neg = 0.001 * 10 ** (-3) # m
# water_viscosity = 0 # m^2/s
# g = 9.798 # m/s^2

# temperature = 20

# water_propierties_df = pd.read_excel("data/water_propierties/Propiedades_agua.xlsx") # Load table for water densities at different temperatures

# water_propierties = water_propierties_df[water_propierties_df['Temp. [°C]'] == temperature]

# water_density = float(water_propierties['Densidad [kg/m3]'].iloc[0])

# water_viscosity = float(water_propierties['Viscocidad cinematica [m²/s]'].iloc[0])

# print(water_propierties)
# # print()


# z1 = 0.97
# z2 = 1.625
# suction_tube_area = ((51.8 * 10 ** (-3)) / 2) ** 2 * np.pi # m^2
# discharge_tube_area = ((38.8 * 10 ** (-3)) / 2) ** 2 * np.pi # m^2

# flow_velocity_suction   = flow / suction_tube_area   / 60000 # m/s
# flow_velocity_discharge = flow / discharge_tube_area / 60000 # m/s

# # Loses for rotodynamic pumps

# # Suction
# L_s = 0.5 # m
# D_s = 51.8 * 10 ** (-3) # m
# sum_k_s = 11.65 + 0.05
# e_s = e_mang_trans


# # Discharge loses 
# D_d_r = 38.8 / 25.4 # in
# sum_k_d_r = 11.65 + 1.5 + 1.4 * (D_d_r ** (-0.53))

# discharge_loses = (sum_k_d_r) * flow_velocity_discharge ** 2 / (2*g) # m

# velocity_head_1 = (flow_velocity_suction  )**2 / (2*g) # m
# velocity_head_2 = (flow_velocity_discharge)**2 / (2*g) # m

# # Suction loses ****************************
# f_s = haalandCalculations(e_s, D_s, water_viscosity, velocity_head_1)
# suction_loses = (f_s * (L_s / D_s) + sum_k_s) * velocity_head_1 ** 2 / (2*g) # m 





# total_suction_head   = z1 + np.array([-1, -1.1, -1.1, -1.1, -1.1]) /14.5038 * (100000) / (water_density * g) + velocity_head_1 - suction_loses
# total_discharge_head = z2 + pressure_out * (100000)/ 14.5038/ (water_density * g) + velocity_head_2 + discharge_loses


# pump_total = total_discharge_head - total_suction_head

# # print(f"suction_loses: {suction_loses}")
# # print(f"discharge_loses: {discharge_loses}")
# # print(f"water_viscosity: {water_viscosity}")
# # print(f"water_density: {water_density}")
# print(f"pump_total: {pump_total}")
# print(f"flow: {flow}")

# plotter(flow, pump_total, "Flujo vs Cabeza", "Flujo (L/min)", "Cabeza (m)")






# # plotter(flow, pressure, "FlowVsHead.png","Flujo vs Cabeza","Flujo (L/min)","Cabeza (m)")



# {'pump_type': 'roto', 'service_order': 'Hola', 'date': 'Estas', 'delegate': 'Como', 'model': '', 'motor_speed': 0, 'power': 0, 'parking_slot': 0, 'test_number': 0, 
# 'flow': [81.40308247675284, 76.87719861512545, 75.56224395551867, 64.93900926160197, 55.79007037986772], 
# 'pressure': [0.0, 0.0, 0.0, 0.0, 0.0], 
# 'velocity': [0.04603994525571119, 0.04106276561835549, 0.039670053906341526, 0.029299783718483713, 0.021625537768634434], 
# 'elevation': [0.655, 0.655, 0.655, 0.655, 0.655], 
# 'pump_total': [1.9081878164408472, 1.7727238746997027, 1.73481819553421, 1.452564934852466, 1.2436853354847064], 
# 'pump_power': [679.1999999999999, 705.6999999999999, 694.5, 679.9, 657.9], 
# 'pump_efficiency': [0.0, 0.0, 0.0, 0.0, 0.0], 'final_flow': 0, 'final_head': 0, 'final_efficiency': 0, 'total_measurements': 5, 'pump_model': 'Hi'}






















# CABEZAS ============================================
# total_suction_head: -0.13779520386143138
# total_discharge_head: 19.162435681151766
# DATOS ALMACENADOS **********************************
# {'pump_type': 'roto', 'service_order': '', 'date': '', 'delegate': '', 'model': '', 'motor_speed': 0, 'power': 0, 'parking_slot': 0, 'test_number': 0, 'flow': [80.37207876301632], 'pressure': [24.826577662709436], 'velocity': [0.0448811007436066], 'elevation': [0.655], 'pump_total': [19.300230885013196], 'pump_power': [661.76], 'pump_efficiency': [38.27453701287183], 'final_flow': 0, 'final_head': 0, 'final_efficiency': 0, 'total_measurements': 5, 'pump_model': ''}
# -------------------------------------------------------
# actual_step: 1
# Medición actual: 3
# actual_step: 2
# Medición actual: 4
# CABEZAS ============================================
# total_suction_head: 0.040708810830238376
# total_discharge_head: 19.5065786696363
# DATOS ALMACENADOS **********************************
# {'pump_type': 'roto', 'service_order': '', 'date': '', 'delegate': '', 'model': '', 'motor_speed': 0, 'power': 0, 'parking_slot': 0, 'test_number': 0, 'flow': [80.37207876301632, 74.02967090895399], 'pressure': [24.826577662709436, 25.32969357908872], 'velocity': [0.0448811007436066, 0.038077176316566416], 'elevation': [0.655, 0.655], 'pump_total': [19.300230885013196, 19.465869858806062], 'pump_power': [661.76, 685.8600000000001], 'pump_efficiency': [38.27453701287183, 34.30732939071379], 'final_flow': 0, 'final_head': 0, 'final_efficiency': 0, 'total_measurements': 5, 'pump_model': ''}
# -------------------------------------------------------
# actual_step: 2
# Medición actual: 5
# actual_step: 3
# Medición actual: 6
# CABEZAS ============================================
# total_suction_head: 0.33073175332467336
# total_discharge_head: 20.05664917515239
# DATOS ALMACENADOS **********************************
# {'pump_type': 'roto', 'service_order': '', 'date': '', 'delegate': '', 'model': '', 'motor_speed': 0, 'power': 0, 'parking_slot': 0, 'test_number': 0, 'flow': [80.37207876301632, 74.02967090895399, 66.0441703330063], 'pressure': [24.826577662709436, 25.32969357908872, 26.127426923978398], 'velocity': [0.0448811007436066, 0.038077176316566416, 0.030305543360728646], 'elevation': [0.655, 0.655, 0.655], 'pump_total': [19.300230885013196, 19.465869858806062, 19.725917421827717], 'pump_power': [661.76, 685.8600000000001, 673.36], 'pump_efficiency': [38.27453701287183, 34.30732939071379, 31.5912738664471], 'final_flow': 0, 'final_head': 0, 'final_efficiency': 0, 'total_measurements': 5, 'pump_model': ''}
# -------------------------------------------------------
# actual_step: 3
# Medición actual: 7
# actual_step: 4
# Medición actual: 8
# CABEZAS ============================================
# total_suction_head: 0.4542777279412078
# total_discharge_head: 20.288932371533516
# DATOS ALMACENADOS **********************************
# {'pump_type': 'roto', 'service_order': '', 'date': '', 'delegate': '', 'model': '', 'motor_speed': 0, 'power': 0, 'parking_slot': 0, 'test_number': 0, 'flow': [80.37207876301632, 74.02967090895399, 66.0441703330063, 61.9128944972642], 'pressure': [24.826577662709436, 25.32969357908872, 26.127426923978398, 26.465103822809535], 'velocity': [0.0448811007436066, 0.038077176316566416, 0.030305543360728646, 0.02663270716621565], 'elevation': [0.655, 0.655, 0.655, 0.655], 'pump_total': [19.300230885013196, 19.465869858806062, 19.725917421827717, 19.83465464359231], 'pump_power': [661.76, 685.8600000000001, 673.36, 659.88], 'pump_efficiency': [38.27453701287183, 34.30732939071379, 31.5912738664471, 30.386700033079517], 'final_flow': 0, 'final_head': 0, 'final_efficiency': 0, 'total_measurements': 5, 'pump_model': ''}
# -------------------------------------------------------
# actual_step: 4
# Medición actual: 9
# actual_step: 5
# data/imgs
# data/html/report.html
# HTML file 'report.html' generated successfully.
# PDF created at report_0.pdf
# CABEZAS ============================================
# total_suction_head: 0.36270295267026453
# total_discharge_head: 20.12861672025588
# DATOS ALMACENADOS **********************************
# {'pump_type': 'roto', 'service_order': '', 'date': '', 'delegate': '', 'model': '', 'motor_speed': 0, 'power': 0, 'parking_slot': 0, 'test_number': 0, 
# 'flow': [80.37207876301632, 74.02967090895399, 66.0441703330063, 61.9128944972642, 81.13757180109516], 
# 'pressure': [24.826577662709436, 25.32969357908872, 26.127426923978398, 26.465103822809535, 26.197681849238563], 
# 'velocity': [0.0448811007436066, 0.038077176316566416, 0.030305543360728646, 0.02663270716621565, 0.045740100063999777], 
# 'elevation': [0.655, 0.655, 0.655, 0.655, 0.655], 
# 'pump_total': [19.300230885013196, 19.465869858806062, 19.725917421827717, 19.83465464359231, 19.765913767585616], 
# 'pump_power': [661.76, 685.8600000000001, 673.36, 659.88, 640.5200000000001], 
# 'pump_efficiency': [38.27453701287183, 34.30732939071379, 31.5912738664471, 30.386700033079517, 40.8835840332464], 
# 'final_flow': 80.37207876301632, 'final_head': 24.826577662709436, 'final_efficiency': 38.27453701287183, 'total_measurements': 5, 'pump_model': ''}
# -------------------------------------------------------





# CABEZAS ============================================
# total_suction_head: 0.9329227522314817
# total_discharge_head: 41.50928535589648
# DATOS ALMACENADOS **********************************
# {'pump_type': 'roto', 'service_order': '', 'date': '', 'delegate': '', 'model': '', 'motor_speed': 0, 'power': 0, 'parking_slot': 0, 'test_number': 0, 'flow': [80.5778618732867, 72.46017340348098, 64.81229644608973, 55.50125709043111, 47.99218724597655, 40.85957349944416, 36.160751946585286, 45.08251496125297], 'pressure': [2.4062743470107164, 30.406261495056, 39.08161162073122, 45.72863406550798, 50.30653564697713, 54.14336108134709, 56.13089557983643, 56.226079672124406], 'velocity': [0.045111220362061666, 0.03647974849272059, 0.029185552351156253, 0.02140221572520322, 0.016002733919048665, 0.011599539698502402, 0.009085064253113149, 0.014121127308735009], 'elevation': [0.655, 0.655, 0.655, 0.655, 0.655, 0.655, 0.655, 0.655], 'pump_total': [4.743741781233289, 23.93457712913942, 29.624942516692194, 33.832237857372185, 36.6913770151439, 39.112487738327786, 40.350729308921935, 40.576362603665], 'pump_power': [649.6600000000001, 675.3199999999999, 655.36, 626.4800000000001, 600.3399999999999, 589.4000000000001, 573.38, 574.8199999999999], 'pump_efficiency': [9.607124202544098, 41.93322546211819, 47.83852146946626, 48.94057725013871, 47.89388053683717, 44.27329964007989, 41.551724648264674, 51.96275049819323], 'final_flow': 55.50125709043111, 'final_head': 45.72863406550798, 'final_efficiency': 48.94057725013871, 'total_measurements': 8, 'pump_model': ''}
# -------------------------------------------------------
