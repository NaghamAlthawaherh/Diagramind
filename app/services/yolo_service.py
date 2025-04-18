import cv2
from ultralytics import YOLO

# تحميل النموذج
model = YOLO("best.pt")  # تأكد إن ملف النموذج موجود
class_names = ["actor", "use_case"]

def analyze_image(image_path):
    image = cv2.imread(image_path)
    results = model(image)

    actors = 0
    use_cases = 0

    for result in results:
        for det in result.boxes.data.cpu().numpy():
            class_id = int(det[5])
            if class_id >= len(class_names):
                continue
            label = class_names[class_id]
            if label == "actor":
                actors += 1
            elif label == "use_case":
                use_cases += 1

    estimated_days = use_cases * 3
    result_image_path = image_path.replace(".jpg", "_result.jpg").replace(".png", "_result.png")
    results[0].save(filename=result_image_path)

    return {
        "actors": actors,
        "use_cases": use_cases,
        "estimated_days": estimated_days,
        "result_image": result_image_path.replace("\\", "/")
    }
