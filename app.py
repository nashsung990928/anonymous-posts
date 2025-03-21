from flask import Flask, request, jsonify
import requests
import os
from instabot import Bot

app = Flask(__name__)

# 從環境變數取得 DeepSeek API Key
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
IG_USERNAME = os.getenv("IG_USERNAME")
IG_PASSWORD = os.getenv("IG_PASSWORD")

# DeepSeek API 處理函式
def process_text(text):
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {DEEPSEEK_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": text}]
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return "Error processing text."

# 發佈 IG 貼文的函式
def post_to_instagram(text, image_path):
    bot = Bot()
    bot.login(username=IG_USERNAME, password=IG_PASSWORD)
    bot.upload_photo(image_path, caption=text)

@app.route("/submit", methods=["POST"])
def submit_post():
    data = request.json
    text = data.get("text")
    image_path = data.get("image_path")  # 預期用戶會提供圖片的路徑
    
    if not text or not image_path:
        return jsonify({"error": "No text or image provided"}), 400
    
    # 處理文本並發佈到 IG
    processed_text = process_text(text)
    post_to_instagram(processed_text, image_path)
    
    return jsonify({"message": "Post submitted successfully!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
