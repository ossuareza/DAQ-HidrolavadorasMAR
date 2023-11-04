import pdfkit

# Configuration options for WkHTMLtoPDF
options = {
    'page-size': 'Letter',
    'margin-top': '0mm',
    'margin-right': '0mm',
    'margin-bottom': '0mm',
    'margin-left': '0mm',
}

# Input HTML file
input_html = 'report.html'

# Output PDF file
output_pdf = 'output.pdf'

# Convert HTML to PDF
pdfkit.from_file(input_html, output_pdf, options=options)

print(f"PDF created at {output_pdf}")



# from reportlab.lib.pagesizes import letter
# from reportlab.lib import colors
# from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
# from reportlab.platypus.tables import Table, TableStyle
# from reportlab.lib.styles import getSampleStyleSheet

# # Create a PDF document and specify the paper size (e.g., letter)
# doc = SimpleDocTemplate("example.pdf", pagesize=letter)

# # Create a list to hold the content elements
# elements = []

# # Create a sample stylesheet
# styles = getSampleStyleSheet()

# # Add a title to the PDF
# elements.append(Paragraph("Sample PDF Generated with Python", styles['Title']))

# # Add some content
# content = """
# This is a sample PDF generated with Python and the ReportLab library.
# You can add paragraphs, tables, and other elements as needed.
# """

# elements.append(Paragraph(content, styles['Normal']))

# # Add a table
# data = [["Name", "Age", "Location"],
#         ["Alice", 25, "New York"],
#         ["Bob", 30, "Los Angeles"],
#         ["Charlie", 22, "Chicago"]]

# # Create a table and set its style
# table = Table(data)
# table.setStyle(TableStyle([
#     ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
#     ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#     ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#     ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#     ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
#     ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
#     ('GRID', (0, 0), (-1, -1), 1, colors.black),
# ]))

# elements.append(table)

# # Build the PDF document
# doc.build(elements)