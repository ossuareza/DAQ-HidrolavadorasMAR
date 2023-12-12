import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

flowmeter_pin = 4
red_button_pin = 22
green_button_pin = 27


pins = [4, 22, 27]

for i in pins:
    GPIO.setup(i,GPIO.IN, pull_up_down=GPIO.PUD_UP)
    # GPIO.setup(i, GPIO.IN)



def next(button_pin):

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
            print("Green button pressed.")
            #! widget.currentWidget().goToNextTask()
            break

        elif time.time() - first_flank_detected_time >= 3:
            return
        
        previous_state = current_state
        
        # Add a small delay to avoid high CPU usage
        time.sleep(0.01)


def closeApp(button_pin):

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
  
def detectPulses(flowmeter_pin):

    print("Pulso detectado")



if __name__ == '__main__':
    
    flowmeter_pin = 4
    
    GPIO.setup(flowmeter_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(flowmeter_pin, GPIO.RISING, callback = lambda x: detectPulses(flowmeter_pin), bouncetime = 1000)   
    

    # Button pin definitions    ******************************************************************************

    red_button_pin = 22 # Button to close the app
    GPIO.setup(red_button_pin, GPIO.IN)
    GPIO.add_event_detect(red_button_pin, GPIO.FALLING, callback = lambda x: closeApp(red_button_pin), bouncetime = 1000)

    green_button_pin = 27 # Button to close the app
    GPIO.setup(green_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(green_button_pin, GPIO.RISING, callback = lambda x: next(green_button_pin), bouncetime = 1000)

    while True:
        pass
    # print(f"pin {4}: {str(GPIO.input(4))}")
    #if GPIO.input(4) == 0:
     #   print(f"Pulso detectado")
    # if GPIO.input(4) == 1:
    #     print(f"pin {24}: {str(GPIO.input(4))}")
    # for i in pins:
    #     if GPIO.input(i) == 0:
    #         print(f"pin {i}: {str(GPIO.input(i))}")
