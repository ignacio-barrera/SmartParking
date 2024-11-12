import cv2
from ultralytics import solutions

cap = cv2.VideoCapture("data/p3.mp4")
assert cap.isOpened(), "Error reading video file"
w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))

video_writer = cv2.VideoWriter("output.avi", cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))

parking_manager = solutions.ParkingManagement(
    model="runs/detect/train2/weights/best.pt",
    json_file="bounding_boxes.json", 
)

while cap.isOpened():
    ret, im0 = cap.read()
    if not ret:
        break
    im0 = parking_manager.process_data(im0)
    video_writer.write(im0)

cap.release()
video_writer.release()
cv2.destroyAllWindows()