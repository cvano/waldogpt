import yt_dlp
import os
from moviepy.editor import VideoFileClip

def download_and_convert_video(url, output_path):
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': output_path + '.%(ext)s',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    
    # Rename the file to ensure it has .mp4 extension
    for file in os.listdir(output_path):
        if file.endswith('.mp4'):
            os.rename(os.path.join(output_path, file), os.path.join(output_path, 'video.mp4'))
            break

def extract_audio(video_path, audio_path):
    video = VideoFileClip(video_path)
    audio = video.audio
    audio.write_audiofile(audio_path)
    video.close()
    audio.close()

if __name__ == "__main__":
    # This allows the script to be run standalone for testing
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    output_path = "."
    download_and_convert_video(url, output_path)
    extract_audio(os.path.join(output_path, "video.mp4"), "audio.mp3")