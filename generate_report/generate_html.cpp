#include <iostream>
#include <fstream>
#include <string>
#include <wkhtmltox/pdf.h>
#include <cstdlib>

struct characterized_pump { 

        int motor_speed = 0, power = 0, parking_slot = 0;
        std::string serial_number, date, delegate, model;
        long test_number = 0;
        int *flow, *pressure, *velocity, *elevation, *pump_total, *pump_power, *pump_efficiency;
        int final_flow = 0, final_head = 0, final_efficiency = 0;
} ;  

void generate_html(characterized_pump pump, int measure_n){

    wkhtmltopdf_init(false);

    std::ofstream myfile;
    
    myfile.open ("report.html");

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
    ".break-after {\n"
    "    page-break-after: always;\n"
    "}\n"
    "\t\t.new-page {\n"
    "\t\tpage-break-before: always;\n"
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
    // "\t<colgroup span=\"8\" width=\"137\"></colgroup>\n"
    "\t<tr>\n"
    "\t\t<td colspan=2 height=\"50\"><img src=\"logo.png\" alt=\"Hidrolavadoras MAR Image\" width=\"200\" height=\"34\"></td>\n"
    "\t\t<td class=\"td_top\" align=\"center\">Velocidad n (rpm)<br><br>" << std::to_string(pump.motor_speed)  << "</td>\n"
    "\t\t<td class=\"td_top\" align=\"center\">Potencia P(kW)<br><br>" << std::to_string(pump.power) << "</td>\n"
    "\t\t<td class=\"td_top\" colspan=2>N"<< static_cast<char>(0xFA) <<"mero del parqueadero:<br><br><br>" << std::to_string(pump.parking_slot) << "</td>\n"
    "\t\t<td class=\"td_top\" colspan=2>N"<< static_cast<char>(0xFA) <<"mero serial de la bomba:<br><br><br>" + pump.serial_number + "</td>\n"
    "\t\t</tr>\n"
    "\t<!-- <tr>\n"
    "\t\t<td><br></td>\n"
    "\t\t<td><br></td>\n"
    "\t\t<td colspan=2><br></td>\n"
    "\t\t<td colspan=2><br></td>\n"
    "\t\t</tr> -->\n"
    "\t<tr class=\"td_top\">\n"
    "\t\t<td height=\"50\" colspan=2 align=\"left\">Fecha de la prueba:<br><br>" + pump.date + "</td>\n"
    "\t\t<td colspan=2 align=\"left\">Encargado:<br><br>" + pump.delegate + "</td>\n"
    "\t\t<td colspan=2 align=\"left\">N"<< static_cast<char>(0xFA) <<"mero de modelo de la bomba:<br>" + pump.model + "</td>\n"
    "\t\t<td colspan=2 align=\"left\">Test n"<< static_cast<char>(0xFA) <<"mero:<br><br>" + std::to_string(pump.test_number) + "</td>\n"
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
        "\t\t<td align=\"center\">" << std::to_string(pump.flow [i-1]) << "</td>\n"
        "\t\t<td align=\"center\">" << std::to_string(pump.pressure [i-1]) << "</td>\n"
        "\t\t<td align=\"center\">" << std::to_string(pump.velocity [i-1]) << "</td>\n"
        "\t\t<td align=\"center\">" << std::to_string(pump.elevation [i-1]) << "</td>\n"
        "\t\t<td align=\"center\">" << std::to_string(pump.pump_total [i-1]) << "</td>\n"
        "\t\t<td align=\"center\">" << std::to_string(pump.pump_power [i-1]) << "</td>\n"
        "\t\t<td align=\"center\">" << std::to_string(pump.pump_efficiency [i-1]) << "</td>\n"
        "\t</tr>\n";
    }
    
    myfile << "\t<tr>\n"
    "\t\t<td colspan=3 align=\"center\" >Punto de garant"<< static_cast<char>(0xED) <<"a</td>\n"
    "\t\t<td colspan=5 rowspan=4 align=\"left\"><font size=4>Este test fue desarrollado con agua limpia a (Inserte Temperatura) (temperatura ambiente). La cabeza, el flujo y la potencia fueron medidas con instrumentación electrónica y la exactitud de los resultados ha sido corroborada</font></td>\n"
    "\t\t</tr>\n"
    "\t<tr>\n"
    "\t\t<td align=\"center\" >Flujo</td>\n"
    "\t\t<td align=\"center\" >" << std::to_string(pump.final_flow) << "</td>\n"
    "\t\t<td align=\"center\" >m"<< static_cast<char>(0xB3) <<"/s</td>\n"
    "\t\t</tr>\n"
    "\t<tr>\n"
    "\t\t<td align=\"center\" >Cabeza</td>\n"
    "\t\t<td >" << std::to_string(pump.final_head) << "</td>\n"
    "\t\t<td align=\"center\" >m</td>\n"
    "\t\t</tr>\n"
    "\t<tr class=\"break-after\">\n"
    "\t\t<td align=\"center\" >Eficiencia</td>\n"
    "\t\t<td align=\"center\" " << std::to_string(pump.final_efficiency) << "</td>\n"
    "\t\t<td align=\"center\" >%</td>\n"
    "\t\t</tr>\n"
    // "</table>\n"
    // "<table class=\"new-page\" cellspacing=\"0\" border=\"0\">\n"
    // "\t<colgroup span=\"8\" width=\"137\"></colgroup>\n"
    "\t<tr >\n"
    // "\t\t<td colspan=8 height=\"50\" align=\"center\" ><img src=\"FlowVsPower.png\" alt=\"Hidrolavadoras MAR Image\" width=\"900\" height=\"300\"> "
    // "<br> <img src=\"FlowVsHead.png\" alt=\"Hidrolavadoras MAR Image\" width=\"900\" height=\"300\">"
    // "<br> <img src=\"FlowVsEfficiency.png\" alt=\"Hidrolavadoras MAR Image\" width=\"900\" height=\"300\"> </td>\n"
    // "\t\t</tr>\n"
    // "\t<tr>\n"
    "\t\t<td colspan=8 height=\"50\" align=\"center\" ><img src=\"FlowVsHead.png\" alt=\"Hidrolavadoras MAR Image\" width=\"900\" height=\"300\"></td>\n"
    "\t\t</tr>\n"
    "\t<tr>\n"
    "\t\t<td colspan=8 height=\"50\" align=\"center\" ><img src=\"FlowVsEfficiency.png\" alt=\"Hidrolavadoras MAR Image\" width=\"900\" height=\"300\"></td>\n"
    "\t\t</tr>\n"
    "\t<tr>\n"
    "\t\t<td colspan=8 height=\"50\" align=\"center\" ><img src=\"FlowVsEfficiency.png\" alt=\"Hidrolavadoras MAR Image\" width=\"900\" height=\"300\"></td>\n"
    "\t\t</tr>\n"
    "</table>\n"
    "<!-- ************************************************************************** -->\n"
    "</body>\n"
    "\n"
    "</html>\n"
    ""<< std::endl;
    

    myfile.close();

    

    wkhtmltopdf_set_object_setting(os, "page", "report.html");

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
}