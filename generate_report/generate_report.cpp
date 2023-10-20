#include <iostream>
#include <fstream>
#include <string>
#include <wkhtmltox/pdf.h>
#include <cstdlib>



#include "TCanvas.h"
#include "TROOT.h"
#include "TGraphErrors.h"
#include "TF1.h"
#include "TLegend.h"
#include "TArrow.h"
#include "TLatex.h"


int main(int argc, char **argv)
{   
    // std::wofstream file("output.html");
   

    int c = 222;

    // file << L"η (eta) is a Greek letter." << c<<std::endl;

    // Close the file
    // file.close();

    int motor_speed = 0, power = 0, parking_slot = 0;

    // Que tipo de variable usar para serial, encargado, fecha, modelo y número de test
    std::string serial_number, date, delegate, model;

    long test_number = 0; // How to update it?

    int measure_n = 5; // Definir cómo se va a modificar esta variable

    int flow [measure_n], pressure [measure_n], velocity [measure_n], elevation [measure_n], pump_total [measure_n], pump_power [measure_n], pump_efficiency [measure_n];

    int final_flow = 0, final_head = 0, final_efficiency = 0;

    wkhtmltopdf_init(false);

    std::ofstream myfile;
    
    myfile.open ("report.html");

    // std::ofstream myfile("report.html");

    // myfile.imbue(std::locale("en_US.UTF-8"));

    std::string var = "Holis" + std::to_string(c) + "\u03B7";
    std::cout << var;

    wkhtmltopdf_global_settings* gs = wkhtmltopdf_create_global_settings();
    wkhtmltopdf_object_settings* os = wkhtmltopdf_create_object_settings();

    wkhtmltopdf_set_object_setting(os, "load.blockLocalFileAccess", "false");
    wkhtmltopdf_set_object_setting(os, "useLocalLinks", "true");

   

    wkhtmltopdf_converter* converter = wkhtmltopdf_create_converter(gs);
    
    // wkhtmltopdf_object_settings* imageObject = wkhtmltopdf_create_object_settings();
    // wkhtmltopdf_set_object_setting(imageObject, "load.blockLocalFileAccess", "false");
    // wkhtmltopdf_set_object_setting(imageObject, "useLocalLinks", "true");
    // wkhtmltopdf_set_object_setting(imageObject, "page", "prueba.jpg");
    

    // std::string htmlString = "<html><body><h1>Create a PDF in C++ using WKHTMLTOPDF Library</h1></body></html>";

    // std::string htmlString = 
    
    myfile <<"<!DOCTYPE html>\n"
    "\n"
    "<html>\n"
    "<head>\n"
    "\n"
    "\t<style type=\"text/css\">\n"
    "\t\t/* body,div,table,thead,tbody,tfoot,tr,th,td,p { font-family:\"Calibri\"; font-size:x-small }\n"
    "\t\ta.comment-indicator:hover + comment { background:#ffd; position:absolute; display:block; border:1px solid black; padding:0.5em;  } \n"
    "\t\ta.comment-indicator { background:red; display:inline-block; border:1px solid black; width:0.5em; height:0.5em;  } \n"
    "\t\tcomment { display:none;  }  */\n"
    "\n"
    "\t\t@import url('https://fonts.googleapis.com/css?family=Montserrat|Open+Sans|Roboto');\n"
    "\t\ttable{\n"
    "\t\t\twidth: 60%; \n"
    "\t\t\tborder-collapse: collapse;\n"
    "\t\t\tborder-spacing: 0;\n"
    "\t\t\tbox-shadow: 0 2px 15px rgba(64,64,64,.7);\n"
    "\t\t\tborder-radius: 12px 12px 0 0;\n"
    "\t\t\toverflow: hidden;\n"
    "\n"
    "\t\t}\n"
    "\t\ttd , th{\n"
    "\t\t\tpadding: 15px 20px;\n"
    "\t\t\tborder-bottom: 1px solid #000000;\n"
    "\t\t\tborder-left: 1px solid #000000; \n"
    "\t\t\tborder-right: 1px solid #000000\n"
    "\n"
    "\t\t}\n"
    "\t\t.td_top{\n"
    "\t\t\tvertical-align: top;\n"
    "\t\t}\n"
    "\t\ttr{\n"
    "\t\t\tfont-family: 'Montserrat', sans-serif;\n"
    "\t\t\tfont-size: x-small;\n"
    "\t\t}\n"
    "\t\t/* tr:nth-child(even){\n"
    "\t\t\tbackground-color: #eeeeee;\n"
    "\t\t} */\n"
    "\n"
    "\t</style>\n"
    "\t\n"
    "</head>\n"
    "\n"
    "\n"
    "\n"
    "<body>\n"
    "<table cellspacing=\"0\" border=\"0\">\n"
    "\t<colgroup span=\"8\" width=\"137\"></colgroup>\n"
    "\t<tr>\n"
    "\t\t<td colspan=2 height=\"50\"><img src=\"logo.png\" alt=\"Hidrolavadoras MAR Image\" width=\"200\" height=\"34\"></td>\n"
    "\t\t<td class=\"td_top\" align=\"center\">Velocidad n (rpm)<br><br>" << std::to_string(motor_speed)  << "</td>\n"
    "\t\t<td class=\"td_top\" align=\"center\">Potencia P(kW)<br><br>" << std::to_string(power) << "</td>\n"
    "\t\t<td class=\"td_top\" colspan=2>N"<< static_cast<char>(0xFA) <<"mero del parqueadero:<br><br><br>" << std::to_string(parking_slot) << "</td>\n"
    "\t\t<td class=\"td_top\" colspan=2>N"<< static_cast<char>(0xFA) <<"mero serial de la bomba:<br><br><br>" + serial_number + "</td>\n"
    "\t\t</tr>\n"
    "\t<!-- <tr>\n"
    "\t\t<td><br></td>\n"
    "\t\t<td><br></td>\n"
    "\t\t<td colspan=2><br></td>\n"
    "\t\t<td colspan=2><br></td>\n"
    "\t\t</tr> -->\n"
    "\t<tr class=\"td_top\">\n"
    "\t\t<td height=\"50\" colspan=2 align=\"left\">Fecha de la prueba:<br><br>" + date + "</td>\n"
    "\t\t<td colspan=2 align=\"left\">Encargado:<br><br>" + delegate + "</td>\n"
    "\t\t<td colspan=2 align=\"left\">N"<< static_cast<char>(0xFA) <<"mero de modelo de la bomba:<br>" + model + "</td>\n"
    "\t\t<td colspan=2 align=\"left\">Test n"<< static_cast<char>(0xFA) <<"mero:<br><br>" + std::to_string(test_number) + "</td>\n"
    "\t\t</tr>\n"
    "\t<!-- <tr>\n"
    "\t\t<td colspan=2 align=\"center\"><br></td>\n"
    "\t\t<td colspan=2 align=\"center\"><br></td>\n"
    "\t\t<td colspan=2 align=\"center\"><br></td>\n"
    "\t\t<td colspan=2 align=\"center\"><br></td>\n"
    "\t\t</tr> -->\n"
    "\t<tr>\n"
    "\t\t<td rowspan=2 align=\"center\">Medici"<< static_cast<char>(0xF3) <<"n No.</td>\n"
    "\t\t<td rowspan=2 align=\"center\">Flujo Q(m"<< static_cast<char>(0xB3) <<"/s)</td>\n"
    "\t\t<td colspan=4 align=\"center\">Cabeza</td>\n"
    "\t\t<td rowspan=2 align=\"center\">Potencia de entrada P(kW)</td>\n"
    "\t\t<td rowspan=2 align=\"center\">Eficiencia de la bomba (%)</td>\n"
    "\t</tr>\n"
    "\t<tr>\n"
    "\t\t<td align=\"center\">Presi"<< static_cast<char>(0xF3) <<"n est"<< static_cast<char>(0xE1) <<"tica p(kPa)</td>\n"
    "\t\t<td align=\"center\">Velocidad h_v(m)</td>\n"
    "\t\t<td align=\"center\">Elevaci"<< static_cast<char>(0xF3) <<"n z(m)</td>\n"
    "\t\t<td align=\"center\">Cabeza total H(m)</td>\n"
    "\t\t</tr>\n";
    
    for (int i = 1; i <= measure_n; i++){

    myfile << "\t<tr>\n"
        "\t\t<td align=\"center\">" << std::to_string(i) << "</td>\n"
        "\t\t<td align=\"center\">" << std::to_string(flow [i-1]) << "</td>\n"
        "\t\t<td align=\"center\">" << std::to_string(pressure [i-1]) << "</td>\n"
        "\t\t<td align=\"center\">" << std::to_string(velocity [i-1]) << "</td>\n"
        "\t\t<td align=\"center\">" << std::to_string(elevation [i-1]) << "</td>\n"
        "\t\t<td align=\"center\">" << std::to_string(pump_total [i-1]) << "</td>\n"
        "\t\t<td align=\"center\">" << std::to_string(pump_power [i-1]) << "</td>\n"
        "\t\t<td align=\"center\">" << std::to_string(pump_efficiency [i-1]) << "</td>\n"
        "\t</tr>\n";
    }
    
    myfile << "\t<tr>\n"
    "\t\t<td colspan=3 align=\"center\" >Punto de garant"<< static_cast<char>(0xED) <<"a</td>\n"
    "\t\t<td colspan=5 rowspan=4 align=\"left\"><font size=4>Este test fue desarrollado con agua limpia a (Inserte Temperatura) (temperatura ambiente). La cabeza, el flujo y la potencia fueron medidas con instrumentación electrónica y la exactitud de los resultados ha sido corroborada</font></td>\n"
    "\t\t</tr>\n"
    "\t<tr>\n"
    "\t\t<td align=\"center\" >Flujo</td>\n"
    "\t\t<td align=\"center\" >" << std::to_string(final_flow) << "</td>\n"
    "\t\t<td align=\"center\" >m"<< static_cast<char>(0xB3) <<"/s</td>\n"
    "\t\t</tr>\n"
    "\t<tr>\n"
    "\t\t<td align=\"center\" >Cabeza</td>\n"
    "\t\t<td >" << std::to_string(final_head) << "</td>\n"
    "\t\t<td align=\"center\" >m</td>\n"
    "\t\t</tr>\n"
    "\t<tr>\n"
    "\t\t<td align=\"center\" >Eficiencia</td>\n"
    "\t\t<td align=\"center\" " << std::to_string(final_efficiency) << "</td>\n"
    "\t\t<td align=\"center\" >%</td>\n"
    "\t\t</tr>\n"
    "\t<tr>\n"
    "\t\t<td colspan=8 rowspan=6 height=\"240\" align=\"center\" >Grafica 1</td>\n"
    "\t\t</tr>\n"
    "\t<tr>\n"
    "\t\t</tr>\n"
    "\t<tr>\n"
    "\t\t</tr>\n"
    "\t<tr>\n"
    "\t\t</tr>\n"
    "\t<tr>\n"
    "\t\t</tr>\n"
    "\t<tr>\n"
    "\t\t</tr>\n"
    "\t<tr>\n"
    "\t\t<td  colspan=8 rowspan=8 height=\"320\" align=\"center\" >Grafica 2</td>\n"
    "\t\t</tr>\n"
    "\t<tr>\n"
    "\t\t</tr>\n"
    "\t<tr>\n"
    "\t\t</tr>\n"
    "\t<tr>\n"
    "\t\t</tr>\n"
    "\t<tr>\n"
    "\t\t</tr>\n"
    "\t<tr>\n"
    "\t\t</tr>\n"
    "\t<tr>\n"
    "\t\t</tr>\n"
    "\t<tr>\n"
    "\t\t</tr>\n"
    "</table>\n"
    "<!-- ************************************************************************** -->\n"
    "</body>\n"
    "\n"
    "</html>\n"
    ""<< std::endl;
    

    myfile.close();

    

    wkhtmltopdf_set_object_setting(os, "page", "/home/jplazag/generate_report/report.html");

    wkhtmltopdf_add_object(converter, os, NULL);

    // wkhtmltopdf_add_object(converter, imageObject, nullptr);

    
    // wkhtmltopdf_set_object_setting(os, "web.loadImages", "true");

    // wkhtmltopdf_add_object(converter, os, htmlString.c_str());

    wkhtmltopdf_convert(converter);

    

    const unsigned char* pdfData;
    const int pdfLength = wkhtmltopdf_get_output(converter, &pdfData);

    const char* outputPath = "file.pdf";
    std::ofstream outputFile(outputPath, std::ios::binary);
    outputFile.write(reinterpret_cast<const char*>(pdfData), pdfLength);
    outputFile.close();

    wkhtmltopdf_destroy_converter(converter);
    wkhtmltopdf_destroy_object_settings(os);
    wkhtmltopdf_destroy_global_settings(gs);
    wkhtmltopdf_deinit();

    std::cout << "PDF created successfully." << std::endl;

    return 0;
}
