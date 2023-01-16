from flask import Flask, request, render_template, redirect, url_for, send_file
import os, sys
from pdf2docx import parse
from typing import Tuple
from flask_jsglue import JSGlue

UPLOADER_FOLDER = ''
app = Flask(__name__)
app.config['UPLOADER_FOLDER'] = UPLOADER_FOLDER
jsglue = JSGlue(app)

def convert_pdf2docx(input_file:str,output_file:str,pages:Tuple=None):
            if pages:
                pages = [int(i) for i in list(pages) if i.isnumeric()]

            result = parse(pdf_file=input_file,docx_with_path=output_file, pages=pages)
            summary = {
                "File": input_file, "Pages": str(pages), "Output File": output_file
                }

            print("\n".join("{}:{}".format(i, j) for i, j in summary.items()))
            return result

@app.route('/')
@app.route('/index', methods=['GET','POST'])
def index():
    if request.method == "POST":
        # Check if the uploaded file is a PDF
        if 'pdf' not in request.files['filename'].content_type:
            return render_template("index.html", message='Invalid file type. Please upload a PDF.')

        file = request.files['filename']
        if file.filename != '':
            file.save(os.path.join(app.config['UPLOADER_FOLDER'], file.filename))
            input_file = file.filename
            output_file = r"hello.docx"
            convert_pdf2docx(input_file, output_file)
            doc = input_file.split(".")[0] + ".docx"
            lis = doc.replace(" ", "=")
            return render_template("docx.html", variable=lis)
    return render_template("index.html")


@app.route('/docx',methods=['GET','POST'])
def docx():
    if request.method=="POST":
        lis=request.form.get('filename',None)
        lis=lis.replace("="," ")
        return redirect(url_for('download', file_path=lis))
    return  render_template("index.html")

# Add this code
@app.route('/download', methods=['GET'])
def download():
    file_path = request.args.get('file_path')
    return send_file(file_path, as_attachment=True)

if __name__=="__main__":
    app.debug=True
    app.run()
