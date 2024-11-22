import os
import re
import requests
import time
from datetime import datetime, timedelta
import threading
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from datetime import datetime

UPLOAD_FOLDER = "uploads"
COUNT_FILE = "service_counts.txt"
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
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
                file.write("{}: {}\n".format(key, value))


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
    for file in request.files.getlist("file"):
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


@app.route("/get_build_data")
def get_build_date():
    def get_latest_succ_ids(job_name, count=12):
        base_url = f"http://liqingguo:1114f1e5b57e96cc4d677ff0932dfbcd54@10.10.20.45:8080/job/{job_name}/api/json"
        params = {"tree": "builds[number,result]"}
        builds = requests.get(base_url, params=params).json().get("builds", [])
        successful_build_ids = [
            build["number"] for build in builds if build.get("result") == "SUCCESS"
        ][:count]
        return successful_build_ids

    channel_translation = {
        "kujian_and": "国服安卓",
        "kujian_ios": "国服iOS",
        "judian_dreamgp": "海外安卓",
        "judian_dreamios": "海外iOS",
    }

    branch_translation = {
        "origin/trunk_2022_3": "主干",
    }

    build_plan_translate = {"private_test": "内网测试", "release": "正式环境"}

    network_translated = {
        "default": "测试服",
        "private_qa": "qa 服",
        "release": "正式服",
        "private_time": "时间服",
        "private_global": "外服内网",
    }

    lines = [
        "Mahjong_Android_Line1",
        "Mahjong_Android_Line2",
        "Mahjong_Android_Line3",
        "Mahjong_iOS_Line1",
        "Mahjong_iOS_Line2",
        "Mahjong_iOS_Line3",
    ]
    all_data = []
    for line in lines:
        try:
            for job_num in get_latest_succ_ids(line):
                url = f"http://liqingguo:1114f1e5b57e96cc4d677ff0932dfbcd54@10.10.20.45:8080/job/{line}/{job_num}/api/json/"
                response = requests.post(url).json()
                parameter_dict = {
                    param["name"]: param["value"]
                    for action in response.get("actions", [])
                    if action.get("_class") == "hudson.model.ParametersAction"
                    for param in action.get("parameters", [])
                }
                branch = parameter_dict.get("branch")
                if branch != "origin/trunk_2022_3":
                    continue
                channel = parameter_dict.get("channel")
                build_plan = parameter_dict.get("buildPlan")
                network = parameter_dict.get("network")
                build_time = (
                    datetime.utcfromtimestamp(response["timestamp"] / 1000)
                    + timedelta(hours=8)
                ).strftime("%m/%d %H:%M:%S")
                png_url = re.search(
                    r"http://[^\s]+\.png", response.get("description", "")
                )
                png_url = png_url.group(0) if png_url else None

                package_url = re.search(
                    r"http://[^\s]+\.(apk|ipa)(?=>)", response.get("description", "")
                )
                package_url = package_url.group(0) if package_url else None
                os = re.search(r"\.(apk|ipa)$", package_url)
                os = os.group(0)
                jenkins_url = re.search(
                    r"http://10\.10\.20\.45:8080/job/[^/]+/\d+/",
                    response.get("description", ""),
                )
                jenkins_url = jenkins_url.group(0) if jenkins_url else None

                # 翻译数据
                translated_channel = channel_translation.get(channel, [])
                translated_branch = branch_translation.get(branch, [])
                translated_build_plan = build_plan_translate.get(build_plan, [])
                translated_network = network_translated.get(network, [])

                data = {
                    "os": os,
                    "channel": translated_channel,
                    "build_time": build_time,
                    "png_url": png_url,
                    "package_url": package_url,
                    "branch": translated_branch,
                    "build_plan": translated_build_plan,
                    "network": translated_network,
                    "jenkins_url": jenkins_url,
                }
                all_data.append(data)

        except:
            print(f"跳过：检测管线请求失败：{line} 不存在成功的构建")
            continue
        unique_data = {}
    for data in all_data:
        key = (
            str(data["channel"]),
            str(data["branch"]),
            str(data["build_plan"]),
        )
        if key not in unique_data:
            unique_data[key] = data
    data = sorted(unique_data.values(), key=lambda x: x["build_time"], reverse=True)
    return data


if __name__ == "__main__":
    if not os.path.exists(app.config["UPLOAD_FOLDER"]):
        os.makedirs(app.config["UPLOAD_FOLDER"])
    if not os.path.exists(COUNT_FILE):
        with open(COUNT_FILE, "w") as file:
            file.write("file_service_count: 0\ntext_service_count: 0\n")
    app.run(host="10.10.243.201", port=5001)
