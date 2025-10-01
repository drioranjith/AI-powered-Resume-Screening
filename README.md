📝 Job Resume Ranking System

A simple Flask-based web application that helps recruiters and HR professionals quickly identify the most relevant candidates for a job role.

🚀 Features

Upload multiple resumes in PDF format

Enter a job description from the frontend

Backend extracts resume text using PyPDF2

Uses Cosine Similarity + CountVectorizer (Scikit-learn) to calculate how well each resume matches the job description

Generates a CSV file with candidate names and similarity scores

Helps recruiters save time by shortlisting the most suitable candidates

🛠️ Tech Stack

Python (Flask)

PyPDF2 for PDF text extraction

Scikit-learn for text similarity

HTML/CSS (Jinja templates) for frontend

CSV for report download

📂 Project Structure
📦 job-resume-ranker
 ┣ 📂 resumes  # Uploaded resumes (PDFs)
 ┣ 📂 static    
 ┣ 📂 templates        # HTML frontend
 ┃ ┗ index.html
   ┗ result.html
 ┣ app.py              # Main Flask app    
 ┗ README.md           # Project documentation

⚡ How to Run

Clone the repo:

 git clone https://github.com/drioranjith/AI-powered-Resume-Screening/

Install dependencies:

pip install flask PyPDF2 scikit-learn


Run the app:

python app.py


Open browser and go to:

http://127.0.0.1:8000/

📊 Example Output

Upload 5 resumes + enter job description.

App returns a downloadable CSV file like this:

Resume	Score (%)
candidate1.pdf	82.45
candidate2.pdf	75.12
candidate3.pdf	63.88
🎯 Use Case

This tool is useful for:

Recruiters to shortlist candidates faster

Hiring managers to automate first-level screening

Job portals as an added feature to rank applicants
