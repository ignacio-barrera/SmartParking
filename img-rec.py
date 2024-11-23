from flask import Flask, request
import os
from datetime import datetime

app = Flask(__name__)

@app.route('/image', methods=['POST'])
def image():
    # Ruta base para guardar imágenes
    UPLOAD_FOLDER = 'server/images/'
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    # Verificar si la solicitud contiene un archivo
    if 'image' not in request.files:
        return 'No image part', 400

    file = request.files['image']
    if file.filename == '':
        return 'No selected file', 400

    # Crear el nombre del archivo basado en el tiempo y un identificador único
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"uploaded_{timestamp}.jpg"
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    # Guardar el archivo en la carpeta designada
    file.save(file_path)

    print(f"Image successfully saved at: {file_path}")
    return f"Image successfully uploaded to {file_path}", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
