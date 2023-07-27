import os
import logging
from flask import Blueprint, render_template, request, send_file, flash, redirect
from werkzeug.utils import secure_filename
from .convert import convert_fpl_to_fms

main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part in the request')
            return redirect(request.url)

        file = request.files['file']

        # If the user does not select a file, the browser submits an empty file
        if file.filename == '':
            flash('No file selected')
            return redirect(request.url)

        # Check if the file has the correct extension
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            # Make sure the 'uploads' directory exists
            os.makedirs('uploads', exist_ok=True)

            # Save the file in the 'uploads' directory
            filepath = os.path.join('uploads', filename)
            file.save(filepath)

            # Convert the .fpl file to .fms
            output_filepath = os.path.join(
                'uploads', filename.rsplit('.', 1)[0] + '.fms')
            try:
                convert_fpl_to_fms(filepath, output_filepath)
                logging.info(f"Converted {filepath} to {output_filepath}")
            except Exception as e:
                logging.error(f"Failed to convert {filepath}: {e}")
                flash('Failed to convert the file.')
                return redirect(request.url)

            flash('File successfully converted.')

            # Get the absolute path of the output file
            output_filepath_abs = os.path.abspath(output_filepath)

            # Return the .fms file for download
            return send_file(output_filepath_abs, as_attachment=True)

        flash('Invalid file type')
        return redirect(request.url)

    return render_template('index.html')


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'fpl'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
