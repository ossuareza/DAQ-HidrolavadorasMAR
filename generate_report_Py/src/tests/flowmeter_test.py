import RPi.GPIO as GPIO
import time

import numpy as np

time_between_pulses = []
first_pulse_received = False
last_pulse_received_time = 0


start_time_flow_measurement = 0
flow_measurement_started = False
flowmeter_pulses = 0
flow = 0

new_bounce_time = None


def countingFlowPulses():

    global flow_measurement_started, start_time_flow_measurement, flowmeter_pulses

    if not flow_measurement_started:
        flow_measurement_started = True
        start_time_flow_measurement = time.time()
        flowmeter_pulses += 1
        print(f"Pulse number: {flowmeter_pulses}")
    else:
        print(f"Pulse number: {flowmeter_pulses}")
        flowmeter_pulses += 1
        
        if flowmeter_pulses == 3:
            definingFlow()

def definingFlow():
    global flow, flow_measurement_started, flowmeter_pulses
    # if time.time() - start_time_flow_measurement >= flow_measurement_time and flow_measurement_started:
    flow = ((flowmeter_pulses - 1)/ (time.time() - start_time_flow_measurement) ) * 60
    flow_measurement_started = False
    flowmeter_pulses = 0

    print(f"Pulse number: {flowmeter_pulses}")
    print(f"Diferencia de tiempo: {time.time() - start_time_flow_measurement}")
    print(f"Flujo final: {flow}")

    

def detectPulses():
    
    global first_pulse_received, last_pulse_received_time, new_bounce_time
    # Start counting the time between pulses
    if not first_pulse_received:
        first_pulse_received = True
        last_pulse_received_time = time.time()

    # Store the time between pulses, so you can look for a pattern
    elif last_pulse_received_time != 0:
        time_between_pulses.append(time.time() -  last_pulse_received_time)
        last_pulse_received_time = time.time()

        print(time_between_pulses)

    if len(time_between_pulses) > 4:
        new_bounce_time = sum(time_between_pulses[-4:]) / 4 # Take the new bounce time as the average of the times stored

        # ANOTHER ALTERNATIVES
        # new_bounce_time = max(time_between_pulses[-4:]) 

        
    if new_bounce_time is not None:
        print("HO")
        print("Expected Bounce time: ",time.time() - last_pulse_received_time)
        if abs(time.time() - last_pulse_received_time) > new_bounce_time:
            print("LA")
            countingFlowPulses()
    else:
        countingFlowPulses()




if __name__ == '__main__':

    GPIO.setmode(GPIO.BCM)

    flowmeter_pin = 4
        
    GPIO.setup(flowmeter_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(flowmeter_pin, GPIO.RISING, callback = lambda x: detectPulses())   

    while True:
        pass