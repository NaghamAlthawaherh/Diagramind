from flask import Flask, request, send_from_directory
from werkzeug.utils import secure_filename
import os
from yolo_analyzer import analyze_image  # 👈 هذا هو الملف اللي عملته

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file = request.files.get("image")
        if not file:
            return "❌ لم يتم اختيار صورة"

        filename = secure_filename(file.filename)
        image_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(image_path)

        # استخدم YOLO لتحليل الصورة
        result = analyze_image(image_path)

        return f"""
        ✅ عدد الممثلين: {result['actors']}<br>
        ✅ عدد حالات الاستخدام: {result['use_cases']}<br>
        ⏱️ المدة التقديرية: {result['estimated_days']} يوم<br><br>
        <img src="/{result['result_image']}" style="max-width:500px;">
        """

    return '''
    <form method="post" enctype="multipart/form-data">
        <input type="file" name="image"><br><br>
        <input type="submit" value="رفع ومعالجة الصورة">
    </form>
    '''

# @app.route("/uploads/<path:filename>")
# def uploaded_file(filename):
#     return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == "__main__":
    app.run(debug=True)
