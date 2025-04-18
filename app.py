from flask import Flask, render_template, request, send_file
from redactor import redact_all
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    redacted = ""
    summary = {}

    if request.method == "POST":

        text = ""
        if "file" in request.files:
            file = request.files["file"]
            if file.filename != "":
                text = file.read().decode("utf-8")

        if not text and "raw_text" in request.form:
            text = request.form["raw_text"]

        if text:
            redacted = redact_all(text)
            

    return render_template("index.html", redacted=redacted, summary=summary)


if __name__ == "__main__":
    app.run(debug=True)
