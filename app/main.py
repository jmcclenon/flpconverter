import os
import logging
from flask import Flask, request, redirect, send_file, flash, render_template
from werkzeug.utils import secure_filename
from app.convert import convert_fpl_to_fms

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'fpl'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'supersecretkey'

# Set up logging
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            logging.info(f"Uploaded file saved to {filepath}")

            # Try to convert the file
            try:
                output_filename = f"{os.path.splitext(filename)[0]}.fms"
                output_filepath = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
                convert_fpl_to_fms(filepath, output_filepath)
                flash('File successfully converted.')
                logging.info(f"Converted {filepath} to {output_filepath}")
                return send_file(output_filepath, as_attachment=True)
            except Exception as e:
                logging.error(f"Failed to convert {filepath}: {e}")
                flash('An error occurred during conversion.')
                return redirect(request.url)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
