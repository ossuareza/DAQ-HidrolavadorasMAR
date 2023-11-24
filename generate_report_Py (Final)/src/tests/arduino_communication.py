import serial
import time

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
    ser.reset_input_buffer()
    time.sleep(1)
    # ser.write(b"R\n")
    t =time.time()
    while - t + time.time() < 2:
        ser.write(b"R\n")
        pressure_in = ser.readline().decode('utf-8').rstrip()
        pressure_out = ser.readline().decode('utf-8').rstrip()

        print(pressure_in, pressure_out)
    """ while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            print(line) """