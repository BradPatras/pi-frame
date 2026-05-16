#!/usr/bin/env python3
from flask import Flask, flash, jsonify, redirect, send_from_directory, request
from flask_cors import CORS
import os
import yaml
from werkzeug.utils import secure_filename
from PIL import Image
import io

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/images"
CORS(app)


@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory("static", path)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in {
        "jpg",
        "jpeg",
        "png",
        "gif",
        "webp",
    }


@app.route("/api/upload", methods=["POST"])
def upload_image():
    # check if the post request has the file part
    if "file" not in request.files:
        flash("No file part")
        return jsonify({"status": "error", "message": "No file part in request"}), 400
    file = request.files["file"]
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == "":
        flash("No selected file")
        return jsonify({"status": "error", "message": "No file selected"}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # resize image before saving
        image = Image.open(file.stream)
        if image.width > 1920 or image.height > 1080:
            image.thumbnail(size=(1920, 1080), resample=Image.Resampling.LANCZOS)
            image.save(
                os.path.join(app.config["UPLOAD_FOLDER"], filename), format=image.format
            )
        else:
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        return jsonify({"status": "success"}), 200


@app.route("/api/images")
def get_images():
    images_dir = "static/images"
    if os.path.exists(images_dir):
        files = [
            f
            for f in os.listdir(images_dir)
            if f.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".webp"))
        ]
        files.sort()

        image_objects = []
        for f in files:
            image_objects.append({"name": f, "url": f"/static/images/{f}"})

        return jsonify(image_objects)
    return jsonify([])


@app.route("/api/delete_image", methods=["POST"])
def delete_image():
    data = request.json
    image_name = secure_filename(data.get("name"))
    if not image_name:
        return jsonify({"status": "error", "message": "No image name provided"}), 400

    # Prevent directory traversal
    if "/" in image_name or "\\" in image_name:
        return jsonify({"status": "error", "message": "Invalid image name"}), 400

    image_path = os.path.join("static/images", image_name)
    if os.path.exists(image_path):
        try:
            os.remove(image_path)
            return jsonify({"status": "success"})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500
    else:
        return jsonify({"status": "error", "message": "Image not found"}), 404


@app.route("/api/interval")
def get_interval():
    config_path = "static/config.yml"
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
            interval_hrs = config.get("image_interval_hrs", 8)
            interval_ms = interval_hrs * 60 * 60 * 1000
    else:
        interval_ms = 8 * 60 * 60 * 1000  # Default to 8 hours
    return jsonify({"delay": interval_ms})


@app.route("/api/config", methods=["GET", "PUT"])
def config():
    config_path = "static/config.yml"
    config_data = {}

    if request.method == "PUT":
        data = request.json
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                config_data = yaml.safe_load(f) or {}
        config_data["image_interval"] = int(data.get("refreshInterval", 8))
        config_data["image_interval_unit"] = data.get("timeUnit", "hours")
        config_data["color_temperature"] = data.get("colorTemp", "")
        with open(config_path, "w") as f:
            yaml.safe_dump(config_data, f)
        return jsonify({"status": "success"})
    elif request.method == "GET":
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                config = yaml.safe_load(f)
                config_data["refreshInterval"] = str(config.get("image_interval", 8))
                config_data["timeUnit"] = str(
                    config.get("image_interval_unit", "hours")
                )
                config_data["colorTemp"] = str(config.get("color_temperature", ""))
        else:
            config_data = {"refreshInterval": "8", "timeUnit": "hours", "colorTemp": ""}
        return jsonify(config_data)


if __name__ == "__main__":
    # For development only. In production, use: gunicorn -w 2 -b 0.0.0.0:8000 server:app
    print("Development server running at http://localhost:8000/")
    print("For production, use gunicorn instead of Flask's dev server")
    app.run(host="0.0.0.0", port=8000, debug=True)
