# DAQ-HidrolavadorasMAR

## Overview

This software controls the data acquisition system for a hydraulic pump characterization bench. It is designed for companies specializing in the commercialization and maintenance of hydraulic pumps and triplex reciprocating pumps. The system measures and stores pressure and flow data at multiple operating points, generating Pressure vs. Flow, Power vs. Flow, and Efficiency vs. Flow curves to find the point of maximum efficiency. All this information, along with pump data, is condensed into a report, standardizing the testing process and ensuring effective maintenance verification with traceable, repeatable reports for each pump.

## Features

- Data Acquisition: Collects real-time data from sensors.
- Data Processing: Checks stability in measurements and average them.
- Reporting: Generates detailed reports on machine performance.
- Sending reports: Send final report to desired E-mail.
- User interface: Offers a comfortable interface for the user to interact.

## Technologies Used

- Python: Main programming language for data handling and report generation.
- HTML: For pdf generation.
- Shell: Scripting and automation.
- PyQt: User interface.

## Components used
### Electronics
- Raspberry Pi 4B
- Analog-to-Digital Converter (ADC) TAR-ADS1015
- Thermocouple module SEN-TERMO-K
- Voltage converter from 24V to 5V BUCK-2-USB-3A-C
- Current converters (4-20mA to 5V) CONV-4-20MAX0-5V
- Power supply NDR-240-24
- Logic level converter BOD0004

### Sensors
- Pressure transmitters:
    - Trafag EPI8287 (-1 to 12 bar)
    - Trafag EPI8287 (0 to 25 bar)
    - Trafag EPI8287 (0 to 400 bar)
- Flow meters:
    - NWM - MJ-SDC DN 50 flanged
    - NWM - MJ-SDC DN 32
- Thermocouples 
    - 2 Thermocouple type K 0-800°C
- Potentiometers
    - 3 Potentiometers PZEM-004T with range from 0 to 22kW

## Usage

Run the main script to start the user interface for data acquisition:
    
    cd /home/pi/DAQ-HidrolavadorasMAR/generate_report_Py

    /usr/bin/python3 src/user_interface_Qt.py

Or just run the sh file `/home/pi/DAQ-HidrolavadorasMAR/generate_report_Py/src/run_script.sh` with the necessary permissions.

## Video 

Here you can watch how it works with an example:

[![Watch the video](https://img.youtube.com/vi/71RvwS4rxUo/0.jpg)](https://youtu.be/71RvwS4rxUo)
