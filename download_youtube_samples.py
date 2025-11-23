import yt_dlp
import os
import imageio_ffmpeg
os.environ["IMAGEIO_FFMPEG_EXE"] = imageio_ffmpeg.get_ffmpeg_exe()

try:
    from moviepy.editor import AudioFileClip
except ImportError:
    from moviepy.audio.io.AudioFileClip import AudioFileClip

def download_sample(search_query, output_filename):
    # Options for yt-dlp - Download video only
    ydl_opts = {
        'format': 'best', # Download best format (likely mp4/webm)
        'outtmpl': 'temp_video.%(ext)s',
        'noplaylist': True,
        'quiet': True,
    }

    print(f"Searching and downloading: {search_query}...")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Search for the first result
            info = ydl.extract_info(f"ytsearch1:{search_query}", download=True)
            video_ext = info['entries'][0]['ext']
            temp_video_path = f"temp_video.{video_ext}"
            print(f"Downloaded video to {temp_video_path}")
            
            # Extract audio using moviepy
            try:
                print("Extracting audio...")
                audio_clip = AudioFileClip(temp_video_path)
                # Trim to first 2 seconds to get just the "hit"
                audio_clip = audio_clip.subclip(0, 2) 
                audio_clip.write_audiofile(f"{output_filename}.wav", logger=None)
                audio_clip.close()
                print(f"Saved audio to {output_filename}.wav")
            except Exception as e:
                print(f"Error extracting audio: {e}")
            finally:
                # Cleanup video
                if os.path.exists(temp_video_path):
                    os.remove(temp_video_path)

    except Exception as e:
        print(f"Error downloading {search_query}: {e}")

def main():
    if not os.path.exists('sounds'):
        os.makedirs('sounds')

    # Define the samples we want
    samples = [
        ("royalty free edm kick drum sample", "sounds/edm-kick"),
        ("royalty free edm snare drum sample", "sounds/edm-snare"),
        ("royalty free edm bass one shot", "sounds/edm-bass"),
        ("royalty free edm synth lead one shot", "sounds/edm-lead"),
        ("royalty free edm pluck one shot", "sounds/edm-pluck")
    ]

    for query, filename in samples:
        download_sample(query, filename)

if __name__ == "__main__":
    main()
