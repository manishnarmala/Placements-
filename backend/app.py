from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from parser.pdf_extractor import extract_text_from_pdf
from parser.ner_model import extract_info

app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = 'uploads/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    text = extract_text_from_pdf(filepath)
    info = extract_info(text)

    return jsonify(info)

if __name__ == '__main__':
    app.run(debug=True)
