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
    def get_latest_succ_ids(job_name):
        base_url = f"http://liqingguo:1114f1e5b57e96cc4d677ff0932dfbcd54@10.10.20.45:8080/job/{job_name}/api/json"
        params = {"tree": "builds[number,result]"}
        builds = requests.get(base_url, params=params).json().get("builds", [])
        successful_build_ids = [
            build["number"] for build in builds if build.get("result") == "SUCCESS"
        ]
        return successful_build_ids

    channel_translation = {
        "kujian_and": "国服安卓",
        "kujian_ios": "国服iOS",
        "judian_dreamgp": "海外安卓",
        "judian_dreamios": "海外iOS",
        "kujian_wechatminigame": "微信小游戏",
    }

    branch_translation = {
        "origin/trunk_2022_3": "主干",
    }

    build_plan_translate = {
        "private_test": "内网测试",
        "release": "正式环境",
        "automation": "自动化",
    }

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
        "Mahjong_WebGL_Line2",
    ]
    target_hosts = [
        "10.10.243.92",
        "10.10.243.92_branch",
        # "121.36.31.27_test",
        # "121.36.31.27",
    ]
    host_translated = {
        "10.10.243.92": "内网测试网页",
        "10.10.243.92_branch": "分支测试网页",
        # "121.36.31.27_test": "外网测试",
        # "121.36.31.27":"正式外网",
    }
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
                if not isinstance(response.get("description", ""), str):
                    continue
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
                if channel in [
                    "kujian_and",
                    "kujian_ios",
                    "judian_dreamgp",
                    "judian_dreamios",
                ]:
                    png_url = re.search(
                        r"http://[^\s]+\.png", response.get("description", "")
                    ).group(0)
                    package_url = re.search(
                        r"http://[^\s]+\.(apk|ipa)(?=>)",
                        response.get("description", ""),
                    ).group(0)
                    os = re.search(r"\.(apk|ipa)$", package_url).group(0)
                else:
                    png_url = re.search(
                        r"http://[^\s]+\.jpg", response.get("description", "")
                    ).group(0)
                    package_url = None
                    os = "minigame"
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
            # print(f"跳过：检测管线请求失败：{line} 不存在成功的构建")
            continue
    # webgl
    latest_builds = {}
    user_info = {}

    for webgl in get_latest_succ_ids("MahjongWebglUpload"):
        url = f"http://liqingguo:1114f1e5b57e96cc4d677ff0932dfbcd54@10.10.20.45:8080/job/MahjongWebglUpload/{webgl}/api/json/"
        response = requests.get(url).json()
        target_host_value = None
        file_value = None
        username = None
        for action in response.get("actions", []):
            if (
                "_class" in action
                and action["_class"] == "hudson.model.ParametersAction"
            ):
                for param in action.get("parameters", []):
                    if param["name"] == "target_host":
                        target_host_value = param["value"]
                    elif param["name"] == "file":
                        file_value = param["value"]
            if "_class" in action and action["_class"] == "hudson.model.CauseAction":
                for cause in action.get("causes", []):
                    if (
                        "_class" in cause
                        and cause["_class"] == "hudson.model.Cause$UserIdCause"
                    ):
                        username = cause.get("userName", None)
        if target_host_value and file_value:
            if (
                target_host_value in target_hosts
                and target_host_value not in latest_builds
            ):
                latest_builds[target_host_value] = file_value
                if username:
                    user_info[target_host_value] = username
            if len(latest_builds) == len(target_hosts):
                break
        if len(latest_builds) == len(target_hosts):
            break

    for webgl in get_latest_succ_ids("Mahjong_WebGL_Line1"):
        url = f"http://liqingguo:1114f1e5b57e96cc4d677ff0932dfbcd54@10.10.20.45:8080/job/Mahjong_WebGL_Line1/{webgl}/api/json/"
        response = requests.get(url).json()
        for target_host in target_hosts:
            if target_host in latest_builds:
                version = latest_builds[target_host].split("-")[-1].replace(".zip", "")
                if version in response.get("description", ""):
                    parameter_dict = {
                        param["name"]: param["value"]
                        for action in response.get("actions", [])
                        if action.get("_class") == "hudson.model.ParametersAction"
                        for param in action.get("parameters", [])
                    }
                    # branch = parameter_dict.get("branch")
                    branch = parameter_dict.get("branch", "").replace("origin/", "")
                    channel = parameter_dict.get("channel")
                    build_plan = parameter_dict.get("buildPlan")
                    network = parameter_dict.get("network")
                    build_time = (
                        datetime.utcfromtimestamp(response["timestamp"] / 1000)
                        + timedelta(hours=8)
                    ).strftime("%m/%d %H:%M:%S")
                    jenkins_url = re.search(
                        r"http://10\.10\.20\.45:8080/job/[^/]+/\d+/",
                        response.get("description", ""),
                    )
                    jenkins_url = jenkins_url.group(0) if jenkins_url else None

                    # 翻译
                    translated_channel = channel_translation.get(channel, [])
                    translated_build_plan = build_plan_translate.get(build_plan, build_plan)
                    translated_network = network_translated.get(network, [])

                    translated_host = host_translated.get(target_host, [])
                    data = {
                        "os": "web",
                        "channel": translated_host,
                        "build_time": build_time,
                        "branch": branch,
                        "build_plan": translated_build_plan,
                        "network": translated_network,
                        "jenkins_url": jenkins_url,
                        "user": user_info[target_host],
                    }
                    all_data.insert(0, data)
    unique_data = {}
    for data in all_data:
        key = (
            str(data["channel"]),
            str(data["branch"]),
            str(data["build_plan"]),
        )
        if key not in unique_data:
            data["build_plan"] = str(data["build_plan"])
            unique_data[key] = data
    sorted_data = sorted(unique_data.values(), key=lambda x: x["build_plan"])
    return sorted_data


if __name__ == "__main__":
    if not os.path.exists(app.config["UPLOAD_FOLDER"]):
        os.makedirs(app.config["UPLOAD_FOLDER"])
    if not os.path.exists(COUNT_FILE):
        with open(COUNT_FILE, "w") as file:
            file.write("file_service_count: 0\ntext_service_count: 0\n")
    app.run(host="10.10.243.201", port=5001)
