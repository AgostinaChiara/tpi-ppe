import cv2
from ultralytics import YOLO

model = YOLO(r"C:\Users\agoss\Downloads\best (1).pt")

image_path = r"C:\Users\agoss\Downloads\pexels-photo-10202865.jpeg"
image = cv2.imread(image_path)

scale_percent = 20
width = int(image.shape[1] * scale_percent / 100)
height = int(image.shape[0] * scale_percent / 100)
dim = (width, height)

resized_image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

results = model.predict(resized_image, imgsz=640, conf=0.6)

annotated_image = results[0].plot()

cv2.imshow('PPE detect', annotated_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

