from flask import Flask, render_template, request
from redactor import redact_all
from docx import Document
from pdfminer.high_level import extract_text
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def read_uploaded_text(file):
    filename = file.filename
    ext = filename.split(".")[-1].lower()

    if ext == "txt":
        return file.read().decode("utf-8")
    elif ext == "pdf":
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        return extract_text(file_path)
    elif ext == "docx":
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        doc = Document(file_path)
        return "\n".join(p.text for p in doc.paragraphs)
    return ""

@app.route("/", methods=["GET", "POST"])
def index():
    redacted = ""
    summary = {}

    if request.method == "POST":
        text = ""

        if "file" in request.files:
            file = request.files["file"]
            if file.filename != "":
                text = read_uploaded_text(file)

        if not text and "raw_text" in request.form:
            text = request.form["raw_text"]

        if text.strip():
            redacted, _, summary = redact_all(text)

    return render_template("index.html", redacted=redacted, summary=summary)

if __name__ == "__main__":
    app.run(debug=True)
