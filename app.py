import os
from flask import Flask, request, jsonify
from google import genai
from google.genai import types

app = Flask(__name__)

# وەرگرتنی کلیلەکە لە سێرڤەری Railway
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"error": "هیچ نامەیەک نەدراوە"}), 400

    try:
        # پێدانی کەسایەتی ARAyAI لە سیستەمی نوێدا
        sys_instruct = "تۆ ناوت ARAyAI یە، ژیرییەکی دەستکردی کوردییت، بە شێوەیەکی زیرەکانە و بە زمانی کوردی سۆرانی وەڵام دەدەیتەوە."
        config = types.GenerateContentConfig(
            system_instruction=sys_instruct,
        )
        
        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contents=user_message,
            config=config
        )
        return jsonify({"reply": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
