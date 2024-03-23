from flask import Flask, render_template, request, url_for
from pdfbuilder import create_cv  # Adjust import path as needed
import spacy

app = Flask(__name__)

nlp = spacy.load("en_core_web_sm")

def extract_info_from_bio(bio_text):
    doc = nlp(bio_text)
    name = None
    skills = []
    experience = []
    education = []

    for ent in doc.ents:
        if ent.label_ == "PERSON" and not name:
            name = ent.text  # Assuming the first PERSON entity could be the name
        elif ent.label_ == "ORG":
            experience.append(ent.text)
        elif ent.label_ in ["GPE", "LOC"]:
            pass
        elif ent.label_ == "SKILL":
            skills.append(ent.text)
        # Add more conditions as needed

    return {
        "name": name,
        "skills": ";".join(skills),
        "experience": ";".join(experience),
        "education": ";".join(education)
    }

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if request.form.get('bio'):  # If bio is provided, extract information from it
            bio = request.form.get('bio')
            extracted_info = extract_info_from_bio(bio)

            name = extracted_info.get('name', 'Unknown Name')
            title = "Generated Title"  # Consider how to handle titles
            email = "Generated Email"  # Consider how to handle emails
            phone = "Generated Phone"  # Consider how to handle phones
            education = extracted_info.get('education', '').split(';')
            experience = extracted_info.get('experience', '').split(';')
            skills = extracted_info.get('skills', '').split(';')
        else:  # Otherwise, use the provided form data
            name = request.form.get('name')
            title = request.form.get('title')
            email = request.form.get('email')
            phone = request.form.get('phone')
            education = request.form.get('education').split(';')
            experience = request.form.get('experience').split(';')
            skills = request.form.get('skills').split(';')

        # Generate the CV and get the path to the created PDF
        pdf_filename = create_cv(name, title, email, phone, education, experience, skills)

        # Construct the URL for the generated PDF to pass to the template
        pdf_url = url_for('static', filename=pdf_filename)

        # Render the result template with the PDF URL
        return render_template('result.html', pdf_url=pdf_url)
    else:
        # Render the form template if method is GET
        return render_template('form.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)
