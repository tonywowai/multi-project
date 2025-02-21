import subprocess
import zipfile
from flask import Flask, render_template, request, redirect, url_for, session
import os
import yaml
# from src.LLM import review_code
# from src.utils.review_utils import load_file
# import google.generativeai as genai

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.secret_key = 'just my random string'  # Needed for session management

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Initialize LLM once with API key
# api_key = "AIzaSyCtuuxWl4_WlBXjbRsMMU9Rh_ccp-KX5qc"
# genai.configure(api_key=api_key)

# generation_config = {
#     "temperature": 0.9,
#     "top_p": 1,
#     "top_k": 1,
#     "max_output_tokens": 2048,
# }

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '':
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(file_path)
                clone_dir = file_path.replace(".zip", "")
                data_zip_dir = file_path
                zip_dir = os.path.join(clone_dir, "data_zip")
                extract_dir = os.path.join(clone_dir, "extract")
                os.makedirs(zip_dir, exist_ok=True)
                os.makedirs(extract_dir, exist_ok=True)

                with zipfile.ZipFile(data_zip_dir, 'r') as zip_ref:
                   
                    zip_ref.extractall(path=extract_dir)
                from pathlib import Path

                requirements_file = Path(f"{extract_dir}/requirements.txt")
                if requirements_file.is_file():
                    subprocess.run(
                        "pip install requirements.txt",
                        shell=True
                    )
                response_info_lines = ""
                requirements_file = Path(f"{extract_dir}/main.py")
                if requirements_file.is_file():
                    command = (
                                "python {file_name} "
                            ).format(
                                    file_name="main.py",
                            )
                    response = subprocess.run(
                        command,
                        shell=True
                    )
                    if response.returncode == 0:
                        response_info_lines = response.stdout.strip()
                    else:
                        response_info_lines = ""
              
                return {"message": "predict completed successfully", "result": response_info_lines}
    
    return render_template('index.html')

# @app.route('/review', methods=['GET'])
# def review():
#     review = session.get('last_review')
#     return render_template('review.html', review=review)

if __name__ == "__main__":
    app.run(debug=True)
