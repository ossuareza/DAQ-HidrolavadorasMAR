from generate_html import generate_html
from generate_pdf import generate_pdf
from plotter import plotter


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

def generate_report(characterized_pump):
    # Generate the graphs of power, pressure, efficiency vs flow
    plotter(characterized_pump["flow"], characterized_pump["pump_power"], "FlowVsPower.png","Flujo vs Potencia","Flujo (L/min)","Potencia (kW)")
    plotter(characterized_pump["flow"], characterized_pump["pressure"], "FlowVsHead.png","Flujo vs Cabeza","Flujo (L/min)","Cabeza (m)")
    plotter(characterized_pump["flow"], characterized_pump["pump_efficiency"], "FlowVsEfficiency.png","Flujo vs Eficiencia","Flujo (L/min)","Eficiencia (%)")

    # Generate a html file that is going to be used as a base for the pdf generation
    generate_html(characterized_pump)

    # Generate the final report in pdf
    generate_pdf(characterized_pump["test_number"])