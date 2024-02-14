from scipy.optimize import minimize
from scipy.interpolate import CubicSpline
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os
import sys

script_path = os.path.abspath(sys.argv[0])
src_path = os.path.dirname(script_path)
directory_path = os.path.dirname(src_path)

class Plotter():

    def __init__(self, x_data, y_data, title, x_label, y_label, file_name, degree):
        self.x_data = x_data
        self.y_data = y_data
        self.title = title
        self.x_label = x_label
        self.y_label = y_label
        self.file_name = file_name
        self.degree = degree

    # Curve model (polynomial of degree 2)
    def curve_model(self, x, params):
        return params[0] * (x)**2 + params[1] * x + params[2]

    # Objective function
    def objective(self, params):
        return sum((self.curve_model(x, params) - y)**2 for x, y in zip(self.x_data[1:], self.y_data[1:]))

    # Constraint function
    def constraint(self, params):
        # Derivative at the maximum point should be 0
        # x_max = - params[2] / (2 * params[0])
        return params[1] #x_max

    # def constraint2(self, params):
    #     # Derivative at the maximum point should be 0
    #     return params[2]
    
    def optimization(self):

        # Optimization with constraint
        result = minimize(self.objective, x0=[1, 1, 1], constraints={'type': 'eq', 'fun': self.constraint})

        # Extract optimized parameters
        return result.x

    def plotter(self):

        if self.y_label == "Cabeza (m)":
            if self.degree == 3:
                coefficients = self.optimization()
                curve = np.poly1d(coefficients)

                x_curve = np.linspace(0, max(self.x_data), 100)
                y_curve = curve(x_curve)
            
            elif self.degree == 1:
                print("self.y_data 1: ", self.y_data)
                self.y_data = [np.mean(self.y_data ) ] * 3

                # print("self.y_data 2: ", self.y_data)
                # coefficients = np.polyfit(self.x_data, self.y_data, self.degree)
                # curve = np.poly1d(coefficients)

                x_curve = np.linspace(0, max(self.x_data), 100)
                y_curve = np.array([self.y_data[0]] * len(x_curve))
        else:
            try:
                coefficients = np.polyfit(self.x_data, self.y_data, self.degree)
                curve = np.poly1d(coefficients)

                # Generate more points on the curve for a smoother plot
                x_curve = np.linspace(min(self.x_data), max(self.x_data), 100)
                y_curve = curve(x_curve)
            
            except:
                x_curve = np.array([])
                y_curve = np.array([])

                print("Problems with the flow variations")

        # Generate more points on the curve for a smoother plot
        
        print("self.y_data 3: ", self.y_data)
        # Plot the interpolated curve
        plt.figure(figsize=(15,5))
        plt.grid(color='0.7', linestyle='--')
        plt.plot(x_curve, y_curve, zorder=1)
        plt.scatter(self.x_data, self.y_data, color='black', zorder=2)
        plt.scatter(x_curve[np.where(y_curve == y_curve.max())][0], y_curve.max(), color='red', zorder=3)
        plt.title(self.title)
        plt.xlabel(self.x_label)
        plt.ylabel(self.y_label)
        path_to_img = os.path.join(directory_path, "data", "imgs", self.file_name)
        # plt.show()
        plt.savefig(path_to_img)

        
# def plotter(x, y, file_name,title,x_label,y_label):
    
#     try:
#         coefficients = np.polyfit(x, y, 3)
#         curve = np.poly1d(coefficients)

#         # Generate more points on the curve for a smoother plot
#         x_curve = np.linspace(min(x), max(x), 100)
#         y_curve = curve(x_curve)
    
#     except:
#         x_curve = []
#         y_curve = []

#         print("Problems with the flow variations")



#     # Plot the interpolated curve
#     plt.figure(figsize=(15,5))
#     plt.grid(color='0.7', linestyle='--')
#     plt.plot(x_curve, y_curve, zorder=1)
#     plt.scatter(x, y, color='black', zorder=2)
#     plt.scatter(x_curve[np.where(y_curve == y_curve.max())][0], y_curve.max(), color='red', zorder=3)
#     plt.title(title)
#     plt.xlabel(x_label)
#     plt.ylabel(y_label)
#     path_to_img = os.path.join("data", "imgs", file_name)
#     plt.savefig(path_to_img)
