import cv2
from picamera2 import Picamera2
from ultralytics import YOLO
from gpiozero import LED

redled = LED(17)
greenled = LED(18)

# Load your exported NCNN model
model = YOLO("yolo11n_ncnn_model", task="detect")

# Recycling rules for supported COCO objects
recyclable = {"bottle"}
non_recyclable = {"banana", "apple", "orange"}

# Set up Raspberry Pi camera
picam2 = Picamera2()
config = picam2.create_preview_configuration(
    main={"size": (640, 480), "format": "RGB888"}
)
picam2.configure(config)
picam2.start()

print("Recycling detection running. Press Q to quit.")

try:
    while True:
        frame = picam2.capture_array()

        # Only detect selected objects
        results = model.predict(
            frame,
            imgsz=320,
            conf=0.80,
            iou=0.30,
            max_det=2,
            classes=[39, 41, 46, 47, 49],
            verbose=False
        )

        display = frame.copy()

        for box in results[0].boxes:
            class_id = int(box.cls[0])
            name = results[0].names[class_id]
            confidence = float(box.conf[0])

            x1, y1, x2, y2 = map(
                int, box.xyxy[0].tolist()
            )

            if name in recyclable:
                category = "POTENTIALLY RECYCLABLE"
                color = (0, 255, 0)
                redled.off()
                greenled.on()

            elif name in non_recyclable:
                category = "NON-RECYCLABLE"
                color = (0, 0, 255)
                greenled.off()
                redled.on()

            else:
                category = "UNKNOWN"
                color = (0, 255, 255)
                greenled.off()
                redled.off()

            cv2.rectangle(
                display,
                (x1, y1), (x2, y2),
                color, 2
            )

            cv2.putText(
                display,
                f"{name}: {category}",
                (x1, max(y1 - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.45,
                color,
                2
            )

        cv2.imshow("AI Recycling Sorter", display)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

except KeyboardInterrupt:
    print("Program stopped")

finally:
    picam2.stop()
    cv2.destroyAllWindows()
