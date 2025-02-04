from flask import Flask, render_template, request, jsonify
import random
import os
import openai
import requests
from moviepy.editor import ImageSequenceClip, TextClip, CompositeVideoClip

app = Flask(__name__)

# OpenAI API Anahtarı
OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"
PEXELS_API_KEY = "YOUR_PEXELS_API_KEY"

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/generate_video', methods=["POST"])
def generate_video():
    topic = request.json.get("topic", None)
    if not topic:
        topic = random.choice(["Bitcoin Fiyat Analizi", "Borsa Yatırımları", "Altın ve Dolar Tahminleri"])
    
    # OpenAI API ile metin oluşturma
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "Sen bir finans analistisiniz."},
                  {"role": "user", "content": f"{topic} hakkında kısa bir özet hazırla."}]
    )
    video_script = response["choices"][0]["message"]["content"]
    
    # Pexels API ile görüntü çekme
    headers = {"Authorization": PEXELS_API_KEY}
    params = {"query": topic, "per_page": 5}
    image_urls = []
    res = requests.get("https://api.pexels.com/v1/search", headers=headers, params=params)
    if res.status_code == 200:
        photos = res.json().get("photos", [])
        image_urls = [photo["src"]["medium"] for photo in photos]
    
    # Görselleri indir ve video oluştur
    image_paths = []
    for i, url in enumerate(image_urls):
        img_path = f"static/image_{i}.jpg"
        img_data = requests.get(url).content
        with open(img_path, "wb") as img_file:
            img_file.write(img_data)
        image_paths.append(img_path)
    
    # MoviePy ile video oluşturma
    clip = ImageSequenceClip(image_paths, fps=1)
    txt_clip = TextClip(video_script, fontsize=24, color='white').set_duration(clip.duration)
    final_video = CompositeVideoClip([clip, txt_clip])
    video_output_path = "static/generated_video.mp4"
    final_video.write_videofile(video_output_path, codec='libx264', fps=1)
    
    return jsonify({"message": "Video başarıyla oluşturuldu!", "video_url": video_output_path})

if __name__ == '__main__':
    app.run(debug=True)
