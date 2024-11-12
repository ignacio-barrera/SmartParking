import cv2
from flask import Flask, request
import os
from datetime import datetime
from ultralytics import YOLO, solutions

app = Flask(__name__)


# Modelo de gestión de estacionamientos utilizando YOLO
parking_manager = solutions.ParkingManagement(
    model="runs/detect/train2/weights/best.pt",
    json_file="bounding_boxes.json", 
)

@app.route('/upload', methods=['POST'])
def upload_image():
    camera_id = request.form.get('camera_id')
    timestamp = request.form.get('timestamp')
    data = request.form.get('data')

    UPLOAD_FOLDER = 'server/images/'
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    if 'image' not in request.files:
        return 'No image part', 400

    file = request.files['image']
    if file.filename == '':
        return 'No selected file', 400

    camera_folder = os.path.join(UPLOAD_FOLDER, camera_id)
    if not os.path.exists(camera_folder):
        os.makedirs(camera_folder)

    timestamp_formatted = datetime.fromisoformat(timestamp).strftime('d%d-m%m_H%H-M%M-S%S')
    filename = f"{camera_id}_{timestamp_formatted}.jpg"
    file_path = os.path.join(camera_folder, filename)
    file.save(file_path)

    # Leer la imagen guardada con OpenCV
    img = cv2.imread(file_path)
    if img is not None:
        # Procesar la imagen como si fuera un frame de video
        processed_img = parking_manager.process_data(img)

        # Guardar o mostrar la imagen procesada
        output_path = os.path.join(camera_folder, f"processed_{filename}")
        cv2.imwrite(output_path, processed_img)
        print(f"Processed image saved at: {output_path}")

    print(f"Received data: {data}")
    return 'Image successfully uploaded and processed', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
