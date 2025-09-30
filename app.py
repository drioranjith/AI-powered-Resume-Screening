from flask import Flask, render_template, request, redirect, url_for, send_from_directory, make_response
import csv
import io
import os
from PyPDF2 import PdfReader
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Folder to store uploaded resumes
UPLOAD_FOLDER = "resumes"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed file extensions for upload
ALLOWED_EXTENSIONS = {"pdf"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# Job description (can be dynamically set via a form in the future)
JOB_DESCRIPTION = """
We are looking for enthusiastic and driven Data Science Interns to join our team for a 3-month internship program. This opportunity provides hands-on experience in data analytics, machine learning, and real-world project development. The internship will be conducted in two phases, with a performance review at the end of the first month to determine continuation for the remaining two months."""

# Function to extract text from a PDF resume
def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Function to rank resumes based on similarity to the job description
def rank_resumes(resume_folder, job_description):
    resumes = {}
    vectorizer = CountVectorizer().fit([job_description])  # Fit the vectorizer on the job description
    
    for filename in os.listdir(resume_folder):
        if filename.endswith(".pdf"):
            file_path = os.path.join(resume_folder, filename)
            resume_text = extract_text_from_pdf(file_path)
            
            # Vectorize the resume text and calculate similarity
            resume_vector = vectorizer.transform([resume_text])
            job_vector = vectorizer.transform([job_description])
            similarity = cosine_similarity(resume_vector, job_vector)[0][0]
            
            resumes[filename] = similarity
    
    # Sort resumes by similarity score
    ranked_resumes = sorted(resumes.items(), key=lambda x: x[1], reverse=True)
    return ranked_resumes

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Read job description from form and rank existing resumes
        job_description = request.form.get("job_description", JOB_DESCRIPTION)
        ranked_resumes = rank_resumes(app.config['UPLOAD_FOLDER'], job_description)
        return render_template("results.html", ranked_resumes=ranked_resumes, job_description=job_description)
    return render_template("index.html")


@app.route("/resume/<path:filename>")
def download_resume(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)


@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        uploaded_files = request.files.getlist("resumes")
        saved_files = []
        for file in uploaded_files:
            if file and allowed_file(file.filename):
                save_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(save_path)
                saved_files.append(file.filename)
        return render_template("upload.html", saved_files=saved_files)
    return render_template("upload.html", saved_files=None)


@app.route("/export", methods=["GET"])
def export_csv():
    job_description = request.args.get("job_description", JOB_DESCRIPTION)
    ranked_resumes = rank_resumes(app.config['UPLOAD_FOLDER'], job_description)

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["resume", "score_percent", "score_raw"])
    for resume, score in ranked_resumes:
        writer.writerow([resume, f"{score * 100:.2f}", f"{score:.6f}"])

    response = make_response(output.getvalue())
    response.headers["Content-Type"] = "text/csv"
    response.headers["Content-Disposition"] = "attachment; filename=ranked_resumes.csv"
    return response

if __name__ == "__main__":
    app.run(port=8000)  # change 8000 to any free port
