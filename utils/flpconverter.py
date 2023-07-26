from flask import Flask, request, send_file, abort, render_template, flash, redirect, url_for
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename
import os
import logging
import xml.etree.ElementTree as ET

app = Flask(__name__)
Bootstrap(app)

app.config['UPLOAD_FOLDER'] = '/app/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'fpl'}
app.secret_key = "3b3533dacf63f08d6fa69d8e36c89cxx"  # Replace with your actual secret key

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part in the request')
            return redirect(request.url)

        file = request.files['file']

        # If the user does not select a file, the browser submits an empty file
        # Check if a file is selected
        if file.filename == '':
            flash('No file selected')
            return redirect(request.url)

        # Check if the file has the correct extension
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # Parse the .flp file
            try:
                tree = ET.parse(file)
            except ET.ParseError:
                flash('Failed to parse the file. Is it a well-formed XML document?')
                return redirect(request.url)

            root = tree.getroot()
            waypoints = root.findall('.//waypoint')

            if not waypoints:
                flash('No waypoints found in the file.')
                return redirect(request.url)

            # Prepare the .fms file
            output_file = os.path.join(app.config['UPLOAD_FOLDER'], os.path.splitext(file.filename)[0] + '.fms')
            with open(output_file, 'w') as f:
                f.write("I\n3 version\n1\n")
                f.write(f"{len(waypoints) - 1}\n")

                # Loop over each waypoint node in the .flp file and write a corresponding line to the .fms file
                for waypoint in waypoints:
                    waypoint_type = waypoint.find('type').text
                    identifier = waypoint.find('identifier').text
                    lat = waypoint.find('lat').text
                    lon = waypoint.find('lon').text

                    # The format of the line depends on the type of the waypoint
                    if waypoint_type == 'AIRPORT':
                        line = "1"
                    elif waypoint_type == 'NDB':
                        line = "2"
                    elif waypoint_type == 'VOR':
                        line = "3"
                    elif waypoint_type == 'INT':
                        line = "11"
                    else:
                        line = "28"

                    line += f" {identifier} 0.000000 {lat} {lon}\n"
                    f.write(line)

            flash('File successfully converted.')
            return send_file(output_file, as_attachment=True)

        flash('Invalid file type')
        return redirect(request.url)

    return render_template('upload.html')

if __name__ == '__main__':
    logging.basicConfig(filename='app.log', level=logging.INFO)
    app.run(debug=True)
