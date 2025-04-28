import os
import cv2
import numpy as np
import io
from PIL import Image as PILImage
from ultralytics import YOLO

from app.models import Image
from flask_login import current_user
from app import db

def analyze_diagram(image_bytes):
    model_path = os.path.join(os.path.dirname(__file__), '../../best1.pt')
    model = YOLO(model_path)

    np_arr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    results = model(image)
    class_names = ["Actor", "Extends", "Includes", "Use Case"]
    CONFIDENCE_THRESHOLD = 0.3
    class_counts = {name: 1 for name in class_names}

    for result in results:
        boxes = result.boxes.xyxy.cpu().numpy()
        class_ids = result.boxes.cls.cpu().numpy()
        scores = result.boxes.conf.cpu().numpy()

        for box, class_id, score in zip(boxes, class_ids, scores):
            class_id = int(class_id)
            if class_id >= len(class_names) or score < CONFIDENCE_THRESHOLD:
                continue

            label = class_names[class_id]
            x1, y1, x2, y2 = map(int, box)
            cropped = image[y1:y2, x1:x2]

            pil_image = PILImage.fromarray(cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB))
            img_byte_arr = io.BytesIO()
            pil_image.save(img_byte_arr, format='PNG')
# 1. حفظ في الفولدر
            uploads_folder = os.path.join(os.path.dirname(__file__), '../../uploads')
            os.makedirs(uploads_folder, exist_ok=True)

            filename = f"{label}_{class_counts[label]}.png"
            file_path = os.path.join(uploads_folder, filename)
            pil_image.save(file_path)  # حفظ الصورة كملف فعلي


            img_bytes = img_byte_arr.getvalue()

            new_img = Image(
                user_id=current_user.id,
                label=label,
                image_data=img_bytes
            )
            db.session.add(new_img)
            db.session.commit()
            class_counts[label] += 1

    return class_counts
