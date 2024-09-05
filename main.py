from ultralytics import YOLO
import cv2

model = YOLO(r"C:\Users\agoss\Downloads\best (1).pt")

cap = cv2.VideoCapture(0)

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

if not cap.isOpened():
    print("Error al abrir la cámara.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error al capturar el fotograma.")
        break

    frame = cv2.flip(frame, 1)

    results = model(frame)

    annotated_frame = results[0].plot()

    cv2.imshow("Detección en tiempo real", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

