import datetime
from pathlib import Path
import importlib.resources
from reportlab.pdfgen import canvas

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from PyPDF2 import PdfReader, PdfWriter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle



def get_output_directory():
    # Get the current script's directory
    base_dir = Path(__file__).parent.parent

    output_dir = base_dir / 'output'
    # Create the directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)  

    return output_dir

def create_pdf(title="Analysis Report"):
    now = datetime.datetime.now()
    output_dir = get_output_directory()

    # Use datetime to create a unique filename
    filename = output_dir / f"{title}_{now.strftime('%Y%m%d_%H%M%S')}.pdf"

    # Generate the PDF
  
    c = canvas.Canvas(str(filename), pagesize=(600, 800))  # Make sure the filename is a string
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 750, title)
    c.save()

    print("PDF report with details will be here: ", filename)
    return filename

def merge_pdfs(base_pdf, additional_pdf):
    # Open the base PDF (the one you are appending to)
    base_reader = PdfReader(base_pdf)
    base_writer = PdfWriter()

    # Add pages from the base PDF to the writer
    for page in range(len(base_reader.pages)):
        base_writer.add_page(base_reader.pages[page])

    # Open the additional PDF (the one you are merging)
    additional_reader = PdfReader(additional_pdf)

    # Add pages from the additional PDF
    for page in range(len(additional_reader.pages)):
        base_writer.add_page(additional_reader.pages[page])

    # Save the merged result
    with open(base_pdf, 'wb') as output_pdf:
        base_writer.write(output_pdf)

# Function to add text to a PDF
def add_text_to_pdf(pdf_filename, text):

    # Convert Path to string if Posix Path object is being passed
    pdf_filename=str(pdf_filename)
    # Create a PDF document
    document = SimpleDocTemplate(pdf_filename, pagesize=letter)
    
    # Set up a style for the text (can customize further)
    styles = getSampleStyleSheet()
    normal_style = styles['Normal']
    
    # Create a paragraph element for the text
    text_paragraph = Paragraph(text, normal_style)
    
    # Add the paragraph to the document with a spacer in between
    story = [text_paragraph, Spacer(1, 12)]  # Spacer adds a gap after the text
    
    # Build the document
    document.build(story)

# Function to add a DataFrame to a PDF as a table
def add_dataframe_to_pdf(pdf_filename, df):
    # Convert the Path object to a string (in case it was passed as a Path)
    pdf_filename = str(pdf_filename)
    
    # Create the PDF document
    document = SimpleDocTemplate(pdf_filename, pagesize=letter)

    table_data = []    
    table_data = [df.columns.tolist()] + df.values.tolist()
    
    # Ensure all elements are Paragraphs (if they are strings) for table compatibility
    styles = getSampleStyleSheet()

    # Convert all strings in the table to Paragraphs (flowable objects)
    formatted_table_data = []
    for row in table_data:
        new_row = []
        for cell in row:
            # If the cell is a string, wrap it in a Paragraph; otherwise, leave it as is
            if isinstance(cell, str):
                new_row.append(Paragraph(cell, styles['Normal']))
            else:
                new_row.append(cell)
        formatted_table_data.append(new_row)

    
    # Create the table from the formatted data
    table = Table(formatted_table_data) 
    
    # Apply styles to the table
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ])
    
    table.setStyle(style)
    
    # Build the document with the table
    pdf_table = []
    pdf_table.append(table)
    document.build(pdf_table)