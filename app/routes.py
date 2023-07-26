from flask import Blueprint, request, send_file
from .convert import convert_fpl_to_fms
import os

main = Blueprint('main', __name__)

@main.route('/convert', methods=['POST'])
def convert():
    # Check if the post request has the file part
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    # If the user does not select a file, the browser submits an empty file
    if file.filename == '':
        return 'No selected file'
    
    if file:
        # Save the uploaded file to a temporary location
        filepath = os.path.join('/tmp', file.filename)
        file.save(filepath)
        
        # Convert the file
        output_path = convert_fpl_to_fms(filepath)
        
        # Send the converted file
        return send_file(output_path, as_attachment=True)

def create_app():
    app = Flask(__name__)
    register_blueprints(app)
    return app

def register_blueprints(app):
    app.register_blueprint(main)
