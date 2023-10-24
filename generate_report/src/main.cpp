#include <iostream>
#include <stdio.h>
#include <stdlib.h>




struct characterized_pump { 

    int motor_speed = 0, power = 0, parking_slot = 0;

    // Que tipo de variable usar para serial, encargado, fecha, modelo y número de test
    std::string serial_number, date, delegate, model;

    long test_number = 0; // How to update it?

    // Definir cómo se va a modificar esta variable

    int *flow, *pressure, *velocity, *elevation, *pump_total, *pump_power, *pump_efficiency;

    int final_flow = 0, final_head = 0, final_efficiency = 0;
} ;  

int generate_html(characterized_pump, int);
void generate_pdf(long);

int main(int argc, char **argv)
{   
        
    int measure_n = 5;
    struct characterized_pump pump_to_test;

    pump_to_test.flow = (int *) malloc(measure_n * sizeof(int));
    pump_to_test.pressure = (int *) malloc(measure_n * sizeof(int));
    pump_to_test.velocity = (int *) malloc(measure_n * sizeof(int));
    pump_to_test.elevation = (int *) malloc(measure_n * sizeof(int));
    pump_to_test.pump_total = (int *) malloc(measure_n * sizeof(int));
    pump_to_test.pump_power = (int *) malloc(measure_n * sizeof(int));
    pump_to_test.pump_efficiency = (int *) malloc(measure_n * sizeof(int));


    if (generate_html(pump_to_test, measure_n) == 1){
        return 1;
    }

    generate_pdf(pump_to_test.test_number);
    
    std::cout << pump_to_test.flow[0] << std::endl;



    return 0;
}
