import os
from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# وەرگرتنی کلیلەکە لە سێرڤەری Railway
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction="تۆ ناوت ARAyAI یە، ژیرییەکی دەستکردی کوردییت، بە شێوەیەکی زیرەکانە و بە زمانی کوردی سۆرانی وەڵام دەدەیتەوە."
)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"error": "هیچ نامەیەک نەدراوە"}), 400

    try:
        response = model.generate_content(user_message)
        return jsonify({"reply": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
