#!/usr/bin/env python3
from flask import Flask, jsonify, send_from_directory
import os
import yaml


app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

@app.route('/api/images')
def get_images():
    images_dir = 'static/images'
    if os.path.exists(images_dir):
        files = [f for f in os.listdir(images_dir) 
                if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp'))]
        files.sort()
        image_paths = [f'images/{f}' for f in files]
        return jsonify(image_paths)
    return jsonify([])

@app.route('/api/interval')
def get_interval():
    config_path = 'static/config.yml'
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
            interval_hrs = config.get('image_interval_hrs', 8)
            interval_ms = interval_hrs * 60 * 60 * 1000
    else:
        interval_ms = 8 * 60 * 60 * 1000  # Default to 8 hours
    return jsonify({'delay': interval_ms})

if __name__ == '__main__':
    # For development only. In production, use: gunicorn -w 2 -b 0.0.0.0:8000 server:app
    print("Development server running at http://localhost:8000/")
    print("For production, use gunicorn instead of Flask's dev server")
    app.run(host='0.0.0.0', port=8000, debug=True)

