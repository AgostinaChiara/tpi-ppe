from ultralytics import YOLO
import cv2
import os
import winsound

model = YOLO(r"C:\Users\agoss\Downloads\best (1).pt")

video_path = r"C:\Users\agoss\Downloads\demonew.mp4"

cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Error al abrir el video.")
    exit()

capture_dir = "capturas"
os.makedirs(capture_dir, exist_ok=True)

scale_percent = 20

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Fin del video o error al capturar el fotograma.")
        break

    width = int(frame.shape[1] * scale_percent / 100)
    height = int(frame.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized_frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)

    results = model(resized_frame)

    class_names = model.names

    detected_classes = [class_names[int(cls)] for cls in results[0].boxes.cls]

    required_equipment = {'casco', 'chaleco'}

    if 'persona' in detected_classes:
        missing_equipment = required_equipment - set(detected_classes)
        if missing_equipment:
            winsound.Beep(1000, 500)

            capture_filename = os.path.join(capture_dir, f"alert_{len(os.listdir(capture_dir)) + 1}.jpg")
            cv2.imwrite(capture_filename, resized_frame)
            print(f"Equipamiento faltante: {', '.join(missing_equipment)}. Captura guardada en: {capture_filename}")

    annotated_frame = results[0].plot()
    cv2.imshow("Detección en tiempo real", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

