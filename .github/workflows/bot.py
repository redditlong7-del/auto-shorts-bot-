import os, requests, time
from BingImageCreator import ImageGen
from moviepy.editor import *
from telegram import Bot

TG_TOKEN = os.getenv('TELEGRAM_TOKEN')
PX_KEY = os.getenv('PIXVERSE_KEY') 
BING = os.getenv('BING_COOKIE')
TOPIC = os.getenv('TOPIC')
CHAT_ID = os.getenv('CHAT_ID')
bot = Bot(TG_TOKEN)

bot.send_message(CHAT_ID, f"🎬 '{TOPIC}' pe video banana start... 10 min lagega")

img_gen = ImageGen(BING)
prompts = [
    f"emotional closeup of {TOPIC}, tears, rainy night, cinematic, 9:16",
    f"{TOPIC}, dramatic rescue scene, people helping, 9:16", 
    f"{TOPIC}, happy ending, safe, warm light, 9:16",
    f"{TOPIC}, crowd emotional, 9:16",
    f"{TOPIC}, hero shot, 9:16"
]
images = []
for i, p in enumerate(prompts):
    bot.send_message(CHAT_ID, f"🖼️ Image {i+1}/5 bana raha...")
    img_gen.save_images(img_gen.get_images(p), f"img_{i}.png")
    images.append(f"img_{i}.png")
    time.sleep(3)

videos = []
for i, img in enumerate(images):
    bot.send_message(CHAT_ID, f"🎥 Video {i+1}/5 bana raha...")
    headers = {"API-KEY": PX_KEY}
    with open(img, 'rb') as f:
        r = requests.post('https://api.pixverse.ai/openapi/v1/video/image', 
                         headers=headers, 
                         files={'image': f}, 
                         data={'prompt': 'slow zoom in, cinematic, 4s'})
    video_id = r.json()['data']['video_id']
    
    for _ in range(30):
        r = requests.get(f'https://api.pixverse.ai/openapi/v1/video/{video_id}', headers=headers)
        if r.json()['data']['status'] == 5:
            url = r.json()['data']['url']
            with open(f"vid_{i}.mp4", 'wb') as f: f.write(requests.get(url).content)
            videos.append(f"vid_{i}.mp4")
            break
        time.sleep(10)

bot.send_message(CHAT_ID, "✂️ Video jod raha hun...")
clips = [VideoFileClip(v) for v in videos]
final = concatenate_videoclips(clips)
final.write_videofile("final.mp4", fps=30)

bot.send_video(CHAT_ID, video=open('final.mp4', 'rb'), caption=f"Ready: {TOPIC}\n#shorts #viral")
bot.send_message(CHAT_ID, "Ho gaya bhai! 🚀")
