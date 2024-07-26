import os
import threading
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from datetime import datetime

UPLOAD_FOLDER = "uploads"
COUNT_FILE = "service_counts.txt"
app = Flask(__name__)
app.config.from_object(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["textarea_content"] = ""
CORS(app, resources={r"/*": {"origins": "*"}})

file_upload_times = {}
lock = threading.Lock()


def read_service_counts():
    with lock:
        if os.path.exists(COUNT_FILE):
            with open(COUNT_FILE, "r") as file:
                lines = file.readlines()
                counts = {}
                for line in lines:
                    key, value = line.strip().split(": ")
                    counts[key] = int(value)
                return counts
        return {"file_service_count": 0, "text_service_count": 0}


def write_service_counts(counts):
    with lock:
        with open(COUNT_FILE, "w") as file:
            for key, value in counts.items():
                file.write(f"{key}: {value}\n")


@app.route("/get_file_service_count")
def get_file_service_count():
    counts = read_service_counts()
    return jsonify({"count": counts["file_service_count"]})


@app.route("/increment_file_service_count")
def increment_file_service_count():
    counts = read_service_counts()
    counts["file_service_count"] += 1
    write_service_counts(counts)
    return jsonify({"count": counts["file_service_count"]})


@app.route("/get_text_service_count", methods=["GET"])
def get_text_service_count():
    counts = read_service_counts()
    return jsonify({"count": counts["text_service_count"]})


@app.route("/increment_text_service_count", methods=["POST"])
def increment_text_service_count():
    counts = read_service_counts()
    counts["text_service_count"] += 1
    write_service_counts(counts)
    return jsonify({"count": counts["text_service_count"]})


@app.route("/file_list")
def get_file_list():
    files = os.listdir(app.config["UPLOAD_FOLDER"])
    file_list = []
    current_time = datetime.now()
    with lock:
        for file in files:
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], file)
            file_size = os.path.getsize(file_path)
            upload_time = file_upload_times.get(file, None)
            if upload_time is not None:
                remaining_time = 5940 - (current_time - upload_time).seconds
                if remaining_time > 0:
                    file_info = {
                        "name": file,
                        "size": file_size,
                        "remainingTime": remaining_time,
                    }
                    file_list.append(file_info)
                else:
                    os.remove(file_path)
                    del file_upload_times[file]
            else:
                os.remove(file_path)
    return jsonify({"files": file_list})


@app.route("/upload", methods=["POST"])
def upload_files():
    saved_files = []
    for file in request.files.getlist('file'):
        if file.filename == "":
            continue
        filename = file.filename
        base_name, ext = os.path.splitext(filename)
        save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        counter = 1
        new_filename = filename
        while os.path.exists(save_path):
            new_filename = f"{base_name}({counter}){ext}"
            save_path = os.path.join(app.config["UPLOAD_FOLDER"], new_filename)
            counter += 1
        file.save(save_path)
        file_upload_times[new_filename] = datetime.now()
        saved_files.append(new_filename)
    increment_file_service_count()
    return jsonify({"success": True, "filenames": saved_files}), 200

@app.route("/download/<filename>")
def download_file(filename):
    uploads_folder = os.path.join(os.getcwd(), app.config["UPLOAD_FOLDER"])
    increment_file_service_count()
    return send_from_directory(uploads_folder, filename, as_attachment=True)


@app.route("/update_textarea", methods=["POST"])
def update_textarea():
    content = request.json.get("content")
    app.config["textarea_content"] = content
    increment_text_service_count()
    return jsonify({"status": "success"})


@app.route("/get_textarea_content")
def get_textarea_content():
    content = app.config["textarea_content"]
    return jsonify({"content": content})


if __name__ == "__main__":
    if not os.path.exists(app.config["UPLOAD_FOLDER"]):
        os.makedirs(app.config["UPLOAD_FOLDER"])
    if not os.path.exists(COUNT_FILE):
        with open(COUNT_FILE, "w") as file:
            file.write("file_service_count: 0\ntext_service_count: 0\n")
    app.run(host="10.10.243.201", port=5001)
