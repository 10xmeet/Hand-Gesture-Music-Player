import yt_dlp
import imageio_ffmpeg
import os
import shutil

def download_sample(search_query, output_filename):
    ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
    print(f"Using ffmpeg at: {ffmpeg_path}")
    
    # Options for yt-dlp
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_filename,
        'ffmpeg_location': os.path.dirname(ffmpeg_path), # yt-dlp expects directory or executable? usually directory or full path. Let's try directory first or just path.
        # Actually yt-dlp 'ffmpeg_location' can be the binary path.
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
        'noplaylist': True,
        'quiet': True,
    }
    
    # We need to ensure we pass the full path to the binary if possible
    # But yt-dlp might look for 'ffmpeg' in that folder. 
    # Let's try to just set the environment variable PATH to include the ffmpeg dir
    os.environ["PATH"] += os.pathsep + os.path.dirname(ffmpeg_path)

    print(f"Searching and downloading: {search_query}...")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Search for the first result
            info = ydl.extract_info(f"ytsearch1:{search_query}", download=True)
            print(f"Downloaded: {info['entries'][0]['title']}")
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
        # We append .wav because postprocessor adds it, but outtmpl needs it without ext sometimes? 
        # yt-dlp handles extensions. Let's just give base name.
        download_sample(query, filename)

if __name__ == "__main__":
    main()
