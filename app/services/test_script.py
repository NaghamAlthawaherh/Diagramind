from image_processor import image_processor

def main():
    image_path = r"C:\Users\User\Downloads\WhatsApp Image 2025-04-08 at 2.48.46 PM.jpeg"


    # معالجة الصورة واكتشاف العناصر
    result = image_processor.process_image(image_path)

    # طباعة النتائج
    print("✅ تم اكتشاف الممثلين (Actors):")
    for actor in result['actor_coordinates']:
        print(actor)

    print("\n✅ تم اكتشاف حالات الاستخدام (Use Cases):")
    for use_case in result['use_case_coordinates']:
        print(use_case)

    print("\n📸 تم حفظ صورة توضح الاكتشاف في:")
    print(result['debug_image_path'])

    # ممكن تجرب أيضاً اختبار الربط بينهم
    connections = image_processor.detect_connections(image_path, result['actor_coordinates'], result['use_case_coordinates'])
    
    print("\n🔗 الاتصالات بين الممثلين وحالات الاستخدام:")
    for actor_index, use_case_indices in connections.items():
        print(f"الممثل {actor_index} مرتبط مع حالات الاستخدام: {use_case_indices}")

if __name__ == "__main__":
    main()
