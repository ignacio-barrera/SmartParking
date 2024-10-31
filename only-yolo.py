import cv2
from ultralytics import YOLO

model = YOLO("runs/detect/train/weights/best.pt")  # Puedes elegir el modelo que prefieras (n, s, m, l, x)

cap = cv2.VideoCapture("data/p3.mp4")
assert cap.isOpened(), "Error leyendo el archivo de video"

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)

    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
            label = int(box.cls) 
            confidence = box.conf.item()
            if label == 3: # Vehículo
                label = "Auto"

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"{label} {confidence:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    cv2.imshow("Vehicle Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
