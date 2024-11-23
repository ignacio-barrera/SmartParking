import cv2
from flask import Flask, request
import os
import json
from datetime import datetime
from ultralytics import solutions
import numpy as np

app = Flask(__name__)

# Modelo de gestión de estacionamientos utilizando YOLO
parking_manager = solutions.ParkingManagement(
    model="best.pt",
    json_file="bounding_boxes.json", 
)

@app.route('/upload', methods=['POST'])
def upload_image():
    camera_id = request.form.get('camera_id')
    timestamp = request.form.get('timestamp')

    if 'image' not in request.files:
        return 'No image part', 400

    file = request.files['image']
    if file.filename == '':
        return 'No selected file', 400

    # Leer la imagen directamente desde el archivo cargado
    file_bytes = file.read()
    np_arr = np.frombuffer(file_bytes, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    if img is not None:
        # Procesar la imagen y obtener información
        parking_manager.model.track(img, persist=True, show=False, classes=[3])
        Available_slots = parking_manager.pr_info['Available']
        Occupancy_slots = parking_manager.pr_info['Occupancy']

        print(f"Available spaces: {Available_slots}")
        print(f"Occupied spaces: {Occupancy_slots}")

        # Procesar la imagen para su almacenamiento final
        processed_img = parking_manager.process_data(img)
        UPLOAD_FOLDER = 'server/images/'
        camera_folder = os.path.join(UPLOAD_FOLDER, camera_id)
        if not os.path.exists(camera_folder):
            os.makedirs(camera_folder)
        timestamp_formatted = datetime.fromisoformat(timestamp).strftime('d%d-m%m_H%H-M%M-S%S')
        filename = f"processed_{camera_id}_{timestamp_formatted}.jpg"
        output_path = os.path.join(camera_folder, filename)
        cv2.imwrite(output_path, processed_img)
        print(f"Processed image saved at: {output_path}")

    return json.dumps({
        "message": "Image successfully uploaded and processed",
        "Available_slots": Available_slots,
        "Occupied": Occupancy_slots
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
