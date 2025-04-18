import cv2
import numpy as np
import pytesseract
import os

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

class OCRService:
    def __init__(self):
        # استخدم PSM 7 لقراءة سطر واحد فقط داخل البوكس — أفضل لحالات الاستخدام
        self.config = '--oem 3 --psm 7'

    def extract_text_from_region(self, image, region):
        x, y, w, h = region['x'], region['y'], region['width'], region['height']
        height, width = image.shape[:2]
        x = max(0, min(x, width - 1))
        y = max(0, min(y, height - 1))
        w = min(w, width - x)
        h = min(h, height - y)

        if w <= 0 or h <= 0:
            return ""

        roi = image[y:y+h, x:x+w]

        # 💡 تكبير النص قبل المعالجة (مفيد جدًا للـ OCR)
        roi = cv2.resize(roi, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

        roi = self.preprocess_for_ocr(roi)

        text = pytesseract.image_to_string(roi, config=self.config).strip()
        return text

    def preprocess_for_ocr(self, image):
        # تحويل للصورة الرمادية
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image

        # تعزيز التباين
        gray = cv2.equalizeHist(gray)

        # Thresholding بسيط (أدق من adaptive أحيانًا)
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # إزالة الضوضاء (Noise)
        kernel = np.ones((1, 1), np.uint8)
        cleaned = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

        return cleaned

    def perform_ocr(self, image_path, actor_regions, use_case_regions):
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Failed to load image: {image_path}")
        
        debug_image = image.copy()

        actor_names = []
        for i, region in enumerate(use_case_regions):
           text = self.extract_text_from_region(image, region)
    
    # فلترة الكلمات المشتبه فيها (روابط، أسهم، تشويش)
           if not text or '<<' in text or '>>' in text or len(text.strip()) <= 3:
              text = f"Use Case {i+1}"
           else:
              text = text.replace('\n', ' ').strip()
              actor_names.append(text)
              x, y = region['x'], region['y']
              cv2.putText(debug_image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        use_case_names = []
        for i, region in enumerate(use_case_regions):
            text = self.extract_text_from_region(image, region)
            text = text.replace('\n', ' ').strip() or f"Use Case {i+1}"
            use_case_names.append(text)
            x, y = region['x'], region['y']
            cv2.putText(debug_image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        debug_dir = os.path.dirname(image_path)
        debug_image_path = os.path.join(debug_dir, "ocr_results.jpg")
        cv2.imwrite(debug_image_path, debug_image)

        return {
            'actor_names': actor_names,
            'use_case_names': use_case_names,
            'debug_image_path': debug_image_path
        }



# Singleton
ocr_service = OCRService()




# import time
# import random

# def perform_ocr(image_path, elements):
#     """
#     Perform OCR on the diagram to extract text from elements
    
#     Args:
#         image_path: Path to the diagram image
#         elements: Previously detected diagram elements
        
#     Returns:
#         Updated diagram elements with text extracted
#     """
#     # Simulate processing delay
#     simulate_processing_delay(2000)
    
#     # In a real implementation, this would use an OCR library (like Tesseract)
#     # to extract text from the image regions defined by the elements
    
#     # For demo purposes, we'll generate some example text based on element types
#     for element in elements:
#         element_type = element.get("type", "")
        
#         if element_type == "actor":
#             # Actor naming follows common patterns
#             actor_names = [
#                 "User", 
#                 "Customer", 
#                 "Administrator", 
#                 "Manager", 
#                 "Supervisor",
#                 "Client",
#                 "System Operator",
#                 "Maintenance Staff",
#                 "Guest"
#             ]
#             element["text"] = random.choice(actor_names)
            
#         elif element_type == "useCase":
#             # Use case text follows "verb + noun" pattern
#             verbs = [
#                 "Manage", 
#                 "Update", 
#                 "Create", 
#                 "Delete", 
#                 "View", 
#                 "Process", 
#                 "Generate", 
#                 "Approve",
#                 "Login to",
#                 "Register for"
#             ]
            
#             nouns = [
#                 "Account", 
#                 "Profile", 
#                 "Order", 
#                 "Request", 
#                 "Report", 
#                 "Settings", 
#                 "Payment",
#                 "System",
#                 "Service",
#                 "Dashboard"
#             ]
            
#             element["text"] = f"{random.choice(verbs)} {random.choice(nouns)}"
            
#         elif element_type == "system":
#             # System boundary labels
#             system_names = [
#                 "System", 
#                 "Application", 
#                 "Platform", 
#                 "Service", 
#                 "Software"
#             ]
#             element["text"] = random.choice(system_names)
            
#     return elements

# def simulate_processing_delay(ms):
#     """Helper function to simulate processing delay"""
#     time.sleep(ms / 1000)