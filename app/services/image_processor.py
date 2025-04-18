from ultralytics import YOLO
import cv2
import os

class ImageProcessor:
    def __init__(self):
        self.model = YOLO("best.pt")  # تأكد إن المسار للمودل صحيح
        self.class_names = ["actor", "use_case"]

    def process_image(self, image_path):
        image = cv2.imread(image_path)
        results = self.model(image)

        actor_coordinates = []
        use_case_coordinates = []

        for result in results:
            for det in result.boxes.data.cpu().numpy():
                x1, y1, x2, y2, _, class_id = det.astype(int)
                label = self.class_names[class_id]

                region = {
                    'x': x1,
                    'y': y1,
                    'width': x2 - x1,
                    'height': y2 - y1
                }

                if label == "actor":
                    actor_coordinates.append(region)
                elif label == "use_case":
                    use_case_coordinates.append(region)

        # حفظ صورة التصنيف
        debug_image_path = image_path.replace(".jpg", "_yolo_result.jpg").replace(".png", "_yolo_result.png")
        results[0].save(filename=debug_image_path)

        return {
            'actor_coordinates': actor_coordinates,
            'use_case_coordinates': use_case_coordinates,
            'debug_image_path': debug_image_path
        }
    def detect_connections(self, image_path, actors, use_cases):
        """
        Detect connections between actors and use cases using proximity (simple heuristic)
        """
        import numpy as np
        connections = {}
        for i, actor in enumerate(actors):
            connections[i] = []
            actor_center_x = actor['x'] + actor['width'] // 2
            actor_center_y = actor['y'] + actor['height'] // 2

            for j, use_case in enumerate(use_cases):
                uc_center_x = use_case['x'] + use_case['width'] // 2
                uc_center_y = use_case['y'] + use_case['height'] // 2

                distance = ((actor_center_x - uc_center_x)**2 + (actor_center_y - uc_center_y)**2)**0.5

                if distance < 300:
                    connections[i].append(j)
        return connections

# Singleton
image_processor = ImageProcessor()


# import cv2
# import numpy as np
# import os

# class ImageProcessor:
#     """
#     Processes use case diagram images to detect actors (stick figures) and use cases (ellipses).
#     Uses OpenCV for shape detection and image segmentation.
#     """
    
#     def __init__(self):

#         # Configuration parameters for detection
#         self.actor_min_aspect_ratio = 1.5  # Actors usually taller than wide
#         self.actor_max_aspect_ratio = 4.0
#         self.use_case_min_aspect_ratio = 0.3  # Use cases usually wider than tall
#         self.use_case_max_aspect_ratio = 1.3
#         self.min_contour_area = 500  # Minimum area to be considered
        
#     def process_image(self, image_path):
#         """
#         Process the image to detect actors and use cases
        
#         Args:
#             image_path: Path to the image file
            
#         Returns:
#             Dictionary containing:
#             - actor_coordinates: List of dictionaries with x, y, width, height
#             - use_case_coordinates: List of dictionaries with x, y, width, height
#         """
#         # Read the image
#         image = cv2.imread(image_path)
#         if image is None:
#             raise ValueError(f"Failed to load image: {image_path}")
        
#         # Resize for processing if image is too large
#         max_dimension = 1200
#         height, width = image.shape[:2]
#         scale_factor = 1.0
#         if max(height, width) > max_dimension:
#             scale_factor = max_dimension / max(height, width)
#             image = cv2.resize(image, (int(width * scale_factor), int(height * scale_factor)))
        
#         # Create a copy for debugging visualization
#         debug_image = image.copy()
        
#         # Convert to grayscale
#         gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
#         # Apply Gaussian blur to reduce noise
#         blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
#         # Apply binary thresholding
#         _, thresh = cv2.threshold(blurred, 200, 255, cv2.THRESH_BINARY_INV)
        
#         # Find contours
#         contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
#         # Filter and classify contours
#         actor_coordinates = []
#         use_case_coordinates = []
        
#         for contour in contours:
#             # Calculate contour area
#             area = cv2.contourArea(contour)
#             if area < self.min_contour_area:
#                 continue
                
#             # Calculate bounding box
#             x, y, w, h = cv2.boundingRect(contour)
            
#             # Calculate aspect ratio
#             aspect_ratio = h / w if w > 0 else 0
            
#             # Classify based on aspect ratio and shape
#             if self.actor_min_aspect_ratio <= aspect_ratio <= self.actor_max_aspect_ratio:
#                 # Likely a stick figure (actor)
#                 actor_coordinates.append({
#                     'x': int(x / scale_factor),
#                     'y': int(y / scale_factor),
#                     'width': int(w / scale_factor),
#                     'height': int(h / scale_factor)
#                 })
                
#                 # Draw actor bounding box
#                 cv2.rectangle(debug_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
#                 cv2.putText(debug_image, "Actor", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                
#             elif self.use_case_min_aspect_ratio <= aspect_ratio <= self.use_case_max_aspect_ratio:
#                 # Calculate circularity/ellipticity
#                 perimeter = cv2.arcLength(contour, True)
#                 circularity = 4 * np.pi * area / (perimeter * perimeter) if perimeter > 0 else 0
                
#                 if circularity > 0.5:  # Likely an oval/ellipse (use case)
#                     use_case_coordinates.append({
#                         'x': int(x / scale_factor),
#                         'y': int(y / scale_factor),
#                         'width': int(w / scale_factor),
#                         'height': int(h / scale_factor)
#                     })
                    
#                     # Draw use case bounding box
#                     cv2.rectangle(debug_image, (x, y), (x + w, y + h), (0, 0, 255), 2)
#                     cv2.putText(debug_image, "Use Case", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        
#         # Save debug image
#         debug_dir = os.path.dirname(image_path)
#         debug_image_path = os.path.join(debug_dir, "detected_shapes.jpg")
#         cv2.imwrite(debug_image_path, debug_image)
        
#         return {
#             'actor_coordinates': actor_coordinates,
#             'use_case_coordinates': use_case_coordinates,
#             'debug_image_path': debug_image_path
#         }
    
#     def detect_connections(self, image_path, actors, use_cases):
#         """
#         Detect connections between actors and use cases
        
#         Args:
#             image_path: Path to the image file
#             actors: List of actor coordinates
#             use_cases: List of use case coordinates
            
#         Returns:
#             Dictionary of connections between actors and use cases
#         """
#         # In a more comprehensive implementation, we would detect lines between
#         # actors and use cases to determine actual connections
        
#         # For now, we'll use a simplified approach based on proximity
#         connections = {}
        
#         # Read the image
#         image = cv2.imread(image_path)
#         if image is None:
#             raise ValueError(f"Failed to load image: {image_path}")
        
#         # For each actor, find the nearest use cases
#         for i, actor in enumerate(actors):
#             connections[i] = []
#             actor_center_x = actor['x'] + actor['width'] // 2
#             actor_center_y = actor['y'] + actor['height'] // 2
            
#             for j, use_case in enumerate(use_cases):
#                 use_case_center_x = use_case['x'] + use_case['width'] // 2
#                 use_case_center_y = use_case['y'] + use_case['height'] // 2
                
#                 # Calculate Euclidean distance
#                 distance = np.sqrt((actor_center_x - use_case_center_x) ** 2 + 
#                                   (actor_center_y - use_case_center_y) ** 2)
                
#                 # If within reasonable proximity (adjust threshold as needed)
#                 # In a real implementation, we'd detect actual lines instead
#                 if distance < 300:
#                     connections[i].append(j)
        
#         return connections

# # Singleton instance
# image_processor = ImageProcessor()