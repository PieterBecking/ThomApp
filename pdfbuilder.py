import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime

def create_cv(name, title, email, phone, education, experience, skills):
    # Ensure the static/CV_pdfs directory exists
    pdfs_dir = "static/CV_pdfs"
    if not os.path.exists(pdfs_dir):
        os.makedirs(pdfs_dir)

    # Generate a unique filename for the PDF
    timestamp = datetime.now().strftime("%Y-%m-%d")
    name_format = name.replace(" ", "_")
    pdf_filename = f"CV_{name_format}_{timestamp}.pdf"
    pdf_path = os.path.join(pdfs_dir, pdf_filename)

    # Create a canvas to draw the PDF
    c = canvas.Canvas(pdf_path, pagesize=letter)
    c.setTitle(f"CV - {name}")

    # Set margins
    left_margin, top_margin = 60, 750
    line_height = 14

    # Personal Information
    c.setFont("Helvetica-Bold", 14)
    c.drawString(left_margin, top_margin, name)
    c.setFont("Helvetica", 11)
    c.drawString(left_margin, top_margin - line_height * 1.5, f"Title: {title}")
    c.drawString(left_margin, top_margin - line_height * 3, f"Email: {email}")
    c.drawString(left_margin, top_margin - line_height * 4.5, f"Phone: {phone}")

    # Education
    c.setFont("Helvetica-Bold", 12)
    c.drawString(left_margin, top_margin - line_height * 6, "Education")
    c.setFont("Helvetica", 11)
    for i, edu in enumerate(education, start=1):
        c.drawString(left_margin, top_margin - line_height * (6 + i * 1.5), edu)

    # Experience
    c.setFont("Helvetica-Bold", 12)
    experience_start_line = 6 + len(education) * 1.5 + 2
    c.drawString(left_margin, top_margin - line_height * experience_start_line, "Experience")
    c.setFont("Helvetica", 11)
    for i, exp in enumerate(experience, start=1):
        c.drawString(left_margin, top_margin - line_height * (experience_start_line + i * 1.5), exp)

    # Skills
    c.setFont("Helvetica-Bold", 12)
    skills_start_line = experience_start_line + len(experience) * 1.5 + 2
    c.drawString(left_margin, top_margin - line_height * skills_start_line, "Skills")
    c.setFont("Helvetica", 11)
    for i, skill in enumerate(skills, start=1):
        c.drawString(left_margin, top_margin - line_height * (skills_start_line + i * 1.5), skill)

    # Finalize and save PDF
    c.showPage()
    c.save()

    # Return the relative path for Flask to serve the PDF
    return os.path.join('CV_pdfs', pdf_filename)

