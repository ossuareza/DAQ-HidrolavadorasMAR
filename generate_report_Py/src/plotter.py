from scipy.interpolate import CubicSpline
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os

def plotter(x, y, file_name,title,x_label,y_label):
    
    try:
        coefficients = np.polyfit(x, y, 3)
        curve = np.poly1d(coefficients)

        # Generate more points on the curve for a smoother plot
        x_curve = np.linspace(min(x), max(x), 100)
        y_curve = curve(x_curve)
    
    except:
        x_curve = []
        y_curve = []

        print("Problems with the flow variations")



    # Plot the interpolated curve
    plt.figure(figsize=(15,5))
    plt.grid(color='0.7', linestyle='--')
    plt.plot(x_curve, y_curve, zorder=1)
    plt.scatter(x, y, color='black', zorder=2)
    plt.scatter(x_curve[np.where(y_curve == y_curve.max())][0], y_curve.max(), color='red', zorder=3)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    path_to_img = os.path.join("data", "imgs", file_name)
    plt.savefig(path_to_img)
