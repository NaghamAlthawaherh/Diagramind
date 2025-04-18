from Diagram_processor import diagram_processor

def main():
    image_path = r"C:\Users\User\Downloads\WhatsApp Image 2025-04-08 at 3.59.10 PM.jpeg" # المسار الكامل للصورة
    diagram_id = "UC001"

    print("🚀 بدء معالجة المخطط...")
    result = diagram_processor.process_diagram(diagram_id, image_path)

   
    print("\n✅ حالات الاستخدام (Use Cases):")
    if result['use_cases']:
       for i, uc in enumerate(result['use_cases']):
        print(f"- Use Case {i + 1}: {uc['name']} (تعقيد: {uc['complexity']})")
    else:
        print("- ⚠️ لم يتم اكتشاف أي حالات استخدام.")

    print("\n📋 المتطلبات (Requirements):")
    for req in result['requirements']:
        print(f"- [{req['req_id']}] ({req['priority']}) {req['description']}")

    print("\n📊 التقدير (Estimation):")
    for key, value in result['estimation'].items():
        print(f"- {key}: {value}")

   
if __name__ == "__main__":
    main()
