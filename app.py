from flask import Flask, render_template, request, jsonify
import random
import os
import openai
import requests
from moviepy import ImageSequenceClip, TextClip, CompositeVideoClip
from dotenv import load_dotenv


app = Flask(__name__)


# .env dosyasını yükle
load_dotenv()
# OpenAI API Anahtarı
openai.api_key = os.getenv("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")
PEXELS_API_KEY = "tZRt6Uq308HvzCEreGdFQsW2VHfbjeA2JGYI790ceVDgYjUXwGacvnSD"

# OpenAI API anahtarını ayarlama
openai.api_key = openai.api_key

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/generate_video', methods=["POST"])
def generate_video():
    topic = request.json.get("topic", None)
    if not topic:
        topic = random.choice(["Bitcoin Fiyat Analizi", "Borsa Yatırımları", "Altın ve Dolar Tahminleri"])

    # OpenAI API ile metin oluşturma (Yeni API yapısı)
    try:
        client = openai.OpenAI()  # Yeni client yapısı
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Gelişmiş model seçimi
            messages=[
                {"role": "system", "content": "Sen bir finans analistisiniz."},
                {"role": "user", "content": f"{topic} hakkında kısa bir özet hazırla."}
            ]


        )
        video_script = response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return jsonify({"error": "OpenAI API hatası: " + str(e)})

    # Pexels API ile görüntü çekme
    headers = {"Authorization": PEXELS_API_KEY}
    params = {"query": topic, "per_page": 5}
    image_urls = []
    try:
        res = requests.get("https://api.pexels.com/v1/search", headers=headers, params=params)
        if res.status_code == 200:
            photos = res.json().get("photos", [])
            image_urls = [photo["src"]["medium"] for photo in photos]
        else:
            return jsonify({"error": "Pexels API hatası"})
    except Exception as e:
        return jsonify({"error": "Pexels API hatası: " + str(e)})

    # Görselleri indir ve video oluştur
    image_paths = []
    try:
        for i, url in enumerate(image_urls):
            img_path = f"static/image_{i}.jpg"
            img_data = requests.get(url).content
            with open(img_path, "wb") as img_file:
                img_file.write(img_data)
            image_paths.append(img_path)
    except Exception as e:
        return jsonify({"error": "Görsel indirme hatası: " + str(e)})

    # MoviePy ile video oluşturma
    try:
        clip = ImageSequenceClip(image_paths, fps=1)
        txt_clip = TextClip(video_script, fontsize=24, color='white').set_duration(clip.duration)
        final_video = CompositeVideoClip([clip, txt_clip])
        video_output_path = "static/generated_video.mp4"
        final_video.write_videofile(video_output_path, codec='libx264', fps=1)
    except Exception as e:
        return jsonify({"error": "Video oluşturma hatası: " + str(e)})

    return jsonify({"message": "Video başarıyla oluşturuldu!", "video_url": video_output_path})

if __name__ == '__main__':
    app.run(debug=True)
