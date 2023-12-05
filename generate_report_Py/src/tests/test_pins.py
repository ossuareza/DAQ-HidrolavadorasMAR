import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

flowmeter_pin = 4
red_button_pin = 22
green_button_pin = 27

pins = [4, 22, 27]

for i in pins:
    GPIO.setup(i,GPIO.IN, pull_up_down=GPIO.PUD_UP)
    # GPIO.setup(i, GPIO.IN)


while True:
    print(f"pin {24}: {str(GPIO.input(4))}")
    # if GPIO.input(4) == 1:
    #     print(f"pin {24}: {str(GPIO.input(4))}")
    # for i in pins:
    #     if GPIO.input(i) == 0:
    #         print(f"pin {i}: {str(GPIO.input(i))}")
