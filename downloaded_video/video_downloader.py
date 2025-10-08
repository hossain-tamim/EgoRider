import os
from pytubefix import YouTube
import cv2


#  Download Only Video (no audio)
def download_video_only(url, path="raw_videos"):
    os.makedirs(path, exist_ok=True)
    yt = YouTube(url)

    print(f"🎬 Title: {yt.title}")
    print(f"📅 Published: {getattr(yt, 'publish_date', 'Not Available')}")
    
    video_stream = yt.streams.filter(adaptive=True, only_video=True, file_extension="mp4") \
                             .order_by("resolution").desc().first()
    if video_stream:
        print("⬇️ Downloading video-only stream...")
        out_file = video_stream.download(output_path=path)
        print(f"✅ Video saved at: {out_file}")
        return out_file
    else:
        print("❌ No video-only stream found!")
        return None


#  Download Only Audio
def download_audio_only(url, path="raw_audios"):
    os.makedirs(path, exist_ok=True)
    yt = YouTube(url)

    audio_stream = yt.streams.filter(only_audio=True, file_extension="mp4").order_by("abr").desc().first()
    if audio_stream:
        print("⬇️ Downloading audio-only stream...")
        out_file = audio_stream.download(output_path=path)
        print(f"✅ Audio saved at: {out_file}")
        return out_file
    else:
        print("❌ No audio-only stream found!")
        return None


#  Extract Frames from Video

def extract_frames(video_path, save_dir="raw_images", frame_interval=50, max_frames=5):
    os.makedirs(save_dir, exist_ok=True)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("❌ Could not open video.")
        return

    frame_count = 0
    saved = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        if frame_count % frame_interval == 0 and saved < max_frames:
            frame_file = os.path.join(save_dir, f"frame_{frame_count}.jpg")
            cv2.imwrite(frame_file, frame)
            print(f"💾 Saved: {frame_file}")
            saved += 1

        if saved >= max_frames:
            break

    cap.release()
    print("✅ Frame extraction complete.")


#  Main Program

if __name__ == "__main__":
    url = input("Enter YouTube URL: ").strip()

    # Step 1: Download Video (only video stream)
    video_file = download_video_only(url)

    # Step 2: Download Audio (only audio stream)
    audio_file = download_audio_only(url)

    # Step 3: Extract Frames from the downloaded video
    if video_file:
        extract_frames(video_file)
