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
  


previous_state = GPIO.input(4)
flank_detected_time = None
pin_number = 4
while True:
    current_state = GPIO.input(4)
    #print(f"pin {4}: {str(GPIO.input(4))}")
    if current_state != previous_state:
        # Flank detected
        flank_detected_time = time.time()
    
    if flank_detected_time is not None and time.time() - flank_detected_time >= 1:
        # Signal has stayed in the new state for at least 1 second
        print("Flank detected and stayed for at least 1 second.")
        break
    
    previous_state = current_state
    
    # Add a small delay to avoid high CPU usage
    time.sleep(0.01)



    # print(f"pin {4}: {str(GPIO.input(4))}")
    #if GPIO.input(4) == 0:
     #   print(f"Pulso detectado")
    # if GPIO.input(4) == 1:
    #     print(f"pin {24}: {str(GPIO.input(4))}")
    # for i in pins:
    #     if GPIO.input(i) == 0:
    #         print(f"pin {i}: {str(GPIO.input(i))}")
