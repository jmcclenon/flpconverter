import os
from flask import Blueprint, render_template, request, send_file
from werkzeug.utils import secure_filename
from .convert import convert_flp_to_fms

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # get the uploaded file
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            # Make sure the 'uploads' directory exists
            os.makedirs('uploads', exist_ok=True)
            # Save the file in the 'uploads' directory
            filepath = os.path.join('uploads', filename)
            file.save(filepath)

            # convert the .flp file to .fms
            output_filepath = os.path.join('uploads', filename.rsplit('.', 1)[0] + '.fms')
            convert_flp_to_fms(filepath, output_filepath)

            # return the .fms file for download
            return send_file(output_filepath, as_attachment=True)

    return render_template('index.html')
