import yt_dlp
import os
import imageio_ffmpeg
import subprocess
import glob

def process_levels():
    url = "https://www.youtube.com/watch?v=owTWCbq_nSk"
    
    # 1. Download
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'temp_levels.%(ext)s',
        'noplaylist': True,
        'quiet': True,
    }

    print(f"Downloading {url}...")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
            files = glob.glob("temp_levels.*")
            if not files:
                print("Error: Download failed.")
                return
            temp_path = files[0]
            print(f"Downloaded to {temp_path}")
            
            # 2. Extract 4 different 10-second loops from the song
            # We'll take sections from different parts to create variety
            ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
            
            if not os.path.exists('sounds'):
                os.makedirs('sounds')
            
            # Define 4 different time sections (10 seconds each)
            sections = [
                (30, 10, 'sounds/levels-1.wav'),   # Drums section
                (50, 10, 'sounds/levels-2.wav'),   # Bass section
                (70, 10, 'sounds/levels-3.wav'),   # Melody section
                (90, 10, 'sounds/levels-4.wav')    # Vocals/full section
            ]
            
            for start_time, duration, output_file in sections:
                print(f"Extracting {output_file} ({start_time}s - {start_time+duration}s)...")
                cmd = [
                    ffmpeg_path, '-y',
                    '-ss', str(start_time),
                    '-t', str(duration),
                    '-i', temp_path,
                    output_file,
                    '-loglevel', 'error'
                ]
                
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"✓ Created {output_file}")
                else:
                    print(f"✗ Error creating {output_file}: {result.stderr}")
            
            # Cleanup
            if os.path.exists(temp_path):
                os.remove(temp_path)
                
            print("\n✓ Done! Levels samples ready in sounds/")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    process_levels()
