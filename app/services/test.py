import cv2
import torch
from ultralytics import YOLO

# Load trained YOLO model
model = YOLO("best.pt")  # Replace with your trained model path

# Load input image
image_path = r"C:\Users\User\Downloads\WhatsApp Image 2025-04-08 at 4.04.11 PM.jpeg" # Replace with your image
image = cv2.imread(image_path)

# Load UML Use Case Diagram Image
image_path = r"C:\Users\User\Downloads\WhatsApp Image 2025-04-08 at 4.04.11 PM.jpeg"   # Replace with your UML image
image = cv2.imread(image_path)

# Run YOLO model on the image
results = model(image)

# Define class names based on training labels
class_names = ["actor", "use_case"]  # Ensure these match your trained classes

# Initialize counts
actors = 0
use_cases = 0

# Process detections
for result in results:
    for det in result.boxes.data.cpu().numpy():
        class_id = int(det[5])  # Class ID
        if class_id >= len(class_names):
            print(f"Warning: Unknown class ID {class_id}")
            continue  # Skip invalid detections

        label = class_names[class_id]

        if label == "actor":
            actors += 1
        elif label == "use_case":
            use_cases += 1

# Estimate Project Duration
def estimate_time(use_cases):
    avg_time_per_use_case = 3  # Assumption: Each use case takes 3 days
    return use_cases * avg_time_per_use_case

estimated_days = estimate_time(use_cases)

# Display results
print(f"Detected {actors} actors and {use_cases} use cases.")
print(f"Estimated project completion time: {estimated_days} days.")

# Show image with detections
# Show image with detections
results[0].show()
