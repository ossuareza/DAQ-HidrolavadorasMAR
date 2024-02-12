import pdfkit
import os
import sys

def generate_pdf(test_number, service_order):

    # Configuration options for WkHTMLtoPDF
    options = {
        'page-size': 'Letter',
        'margin-top': '0mm',
        'margin-right': '0mm',
        'margin-bottom': '0mm',
        'margin-left': '0mm',
        'enable-local-file-access': True
    }

    script_path = os.path.abspath(sys.argv[0])
    src_path = os.path.dirname(script_path)
    directory_path = os.path.dirname(src_path)
    # Input HTML file
    path_to_input_html = os.path.join(directory_path, "data", "html", 'report.html') 

    # Output PDF file
    file_name = f"Reporte_No_{test_number}_Orden_{service_order}.pdf"

    path_to_output_file = os.path.join(directory_path, "data", "report", file_name)

    # Convert HTML to PDF
    pdfkit.from_file(path_to_input_html, path_to_output_file, options=options)

    print(f"PDF created at {file_name}")



    