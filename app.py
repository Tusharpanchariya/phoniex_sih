from flask import Flask, render_template, request, send_file # type: ignore
import pandas as pd # type: ignore
import io
import os
from werkzeug.utils import secure_filename # type: ignore
import traceback
import logging
import requests # type: ignore
import json
app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max-limit

logging.basicConfig(level=logging.DEBUG)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_excel(file):
    df = pd.read_excel(file)
    return df[['author', 'authorID']]
def get_data(authorID):
    params={"engine":"google_scholar_author",
            "author_id": authorID,
            "api_key": "044cd4179486a2ec60c518e279336ea584771cd5286a0d7e64452a184fb22345"
}

    search = requests.get("https://serpapi.com/search",params=params)
    results = search.json()
    author = results["author"]
    interests = results["articles"]
    return interests
def generate_bibtex(df):
    bibtex = ""
    for _, row in df.iterrows():
        bibtex += f"@article{{{row['authorID']},\n"
        bibtex += f"  author = {{{row['author']}}},\n"
        interests= get_data(row['authorID'])
        for interest in interests:
            bibtex += f"  title = {{{interest['title']}}},\n"
            bibtex += f"  link = {{{interest['link']}}},\n"
            bibtex += "}\n\n"
    return bibtex
def generate_excel(df):
    data =[]
    for _, row in df.iterrows():
        authorID =row['authorID']
        author = row['author']
        interests= get_data(authorID)
        data.append({
            "AuthorID": authorID,
            "Author" : author})
        for interest in interests:
            data.append({
                "Title": interest['title'],
                "Link": interest['link']})
    interests_df = pd.DataFrame(data)
    output_file = "author_output.xlsx"
    interests_df.to_excel(output_file,index=False)
    return output_file

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        try:
            if 'file' not in request.files:
                return render_template('index.html', message='No file part')
            file = request.files['file']
            if file.filename == '':
                return render_template('index.html', message='No selected file')
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                
                logging.info(f"File saved: {file_path}")
                
                df = process_excel(file_path)
                
                logging.info(f"Excel processed. Data shape: {df.shape}")
                
                # Generate Excel output
                output = generate_excel(df)               
                # Generate BibTeX output
                bibtex_output = generate_bibtex(df)
                
                os.remove(file_path)  # Remove the uploaded file after processing
                
                return render_template('result.html', excel_data=output, bibtex_data=bibtex_output)
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            logging.error(traceback.format_exc())
            return render_template('index.html', message=f"An error occurred: {str(e)}")
    return render_template('index.html')

@app.route('/download/<filetype>')
def download_file(filetype):
    try:
        if filetype == 'excel':

                
            df = pd.read_excel(request.args.get('data'))            
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='Sheet1')
            output.seek(0)
            return send_file(output, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', as_attachment=True, download_name='output.xlsx')
        elif filetype == 'bibtex':
            bibtex_data = request.args.get('data')
            return send_file(io.BytesIO(bibtex_data.encode()), mimetype='text/plain', as_attachment=True, download_name='output.bib')
    except Exception as e:
        logging.error(f"Download error: {str(e)}")
        logging.error(traceback.format_exc())
        return f"An error occurred during download: {str(e)}", 500

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)
