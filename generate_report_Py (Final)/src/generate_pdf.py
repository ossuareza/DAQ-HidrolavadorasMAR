import pdfkit
import os

def generate_pdf(test_number):

    # Configuration options for WkHTMLtoPDF
    options = {
        'page-size': 'Letter',
        'margin-top': '0mm',
        'margin-right': '0mm',
        'margin-bottom': '0mm',
        'margin-left': '0mm',
        'enable-local-file-access': True
    }

    # Input HTML file
    path_to_input_html = os.path.join("data", "html", 'report.html') 

    # Output PDF file
    file_name = f"report_{test_number}.pdf"

    path_to_output_file = os.path.join("data", "report", file_name)

    # Convert HTML to PDF
    pdfkit.from_file(path_to_input_html, path_to_output_file, options=options)

    print(f"PDF created at {file_name}")



    