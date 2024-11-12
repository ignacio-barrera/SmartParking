from flask import Flask, request
import os
from datetime import datetime

app = Flask(__name__)

UPLOAD_FOLDER = 'images/'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/upload', methods=['POST'])
def upload_image():
    camera_id = request.form.get('camera_id')
    timestamp = request.form.get('timestamp')
    data = request.form.get('data')

    if 'image' not in request.files:
        return 'No image part', 400

    file = request.files['image']
    if file.filename == '':
        return 'No selected file', 400

    camera_folder = os.path.join(UPLOAD_FOLDER, camera_id)
    if not os.path.exists(camera_folder):
        os.makedirs(camera_folder)

    timestamp = datetime.fromisoformat(timestamp).strftime('d%d-m%m_H%H-M%M-S%S')
    filename = f"{camera_id}_{timestamp}.jpg"
    file_path = os.path.join(camera_folder, filename)
    file.save(file_path)

    print(f"Received data: {data}")

    return 'Image successfully uploaded', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
