#include <iostream>
#include <fstream>
#include <string>
#include <wkhtmltox/pdf.h>
// #include <cstdlib>


void generate_pdf(long test_number){

    wkhtmltopdf_init(false);

   

    wkhtmltopdf_global_settings* gs = wkhtmltopdf_create_global_settings();
    wkhtmltopdf_object_settings* os = wkhtmltopdf_create_object_settings();

    wkhtmltopdf_set_object_setting(os, "load.blockLocalFileAccess", "false");
    wkhtmltopdf_set_object_setting(os, "useLocalLinks", "true");

    wkhtmltopdf_converter* converter = wkhtmltopdf_create_converter(gs);
    wkhtmltopdf_set_object_setting(os, "page", "data/html/report_model.html");
    wkhtmltopdf_add_object(converter, os, NULL);
    wkhtmltopdf_convert(converter);

    const unsigned char* pdfData;
    const int pdfLength = wkhtmltopdf_get_output(converter, &pdfData);
    
    std::string outputPath = "data/report/report_";
    outputPath += std::to_string(test_number);
    outputPath += ".pdf";
    std::ofstream outputFile(outputPath, std::ios::binary);
    outputFile.write(reinterpret_cast<const char*>(pdfData), pdfLength);
    outputFile.close();

    wkhtmltopdf_destroy_converter(converter);
    wkhtmltopdf_destroy_object_settings(os);
    wkhtmltopdf_destroy_global_settings(gs);
    wkhtmltopdf_deinit();
    
    std::cout << "PDF created successfully." << std::endl;
}