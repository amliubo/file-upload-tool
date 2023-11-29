import os
import threading
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

UPLOAD_FOLDER = 'uploads'
app = Flask(__name__)
app.config.from_object(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app, resources={r'/*': {'origins': '*'}})

@app.route('/file_list')
def get_file_list():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    file_list = [{'name': file, 'size': os.path.getsize(os.path.join(app.config['UPLOAD_FOLDER'], file))} for file in files]
    return jsonify({'files': file_list})

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'status': 'error', 'message': 'No file provided'}), 400

    files = request.files.getlist('file')

    for file in files:
        if file.filename == '':
            return jsonify({'status': 'error', 'message': 'No selected file'}), 400

        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)

    return jsonify({'status': 'success', 'message': 'Files uploaded successfully'})

@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename, as_attachment=True)

def clear_upload_folder():
    print("Clearing UPLOAD_FOLDER")
    for file_name in os.listdir(app.config['UPLOAD_FOLDER']):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Error deleting file {file_path}:{e}")

def perform_cleanup():
    clear_upload_folder()
    timer = threading.Timer(28800, perform_cleanup)
    timer.start()
    
if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    perform_cleanup()
    app.run(port=5001)