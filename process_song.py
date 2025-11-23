import yt_dlp
import os
import imageio_ffmpeg
import subprocess
import glob

def download_and_process():
    url = "https://www.youtube.com/watch?v=5gga8E43clk"
    
    # 1. Download
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'temp_animals.%(ext)s',
        'noplaylist': True,
        'quiet': True,
    }

    print(f"Downloading {url}...")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
            # Find the downloaded file
            files = glob.glob("temp_animals.*")
            if not files:
                print("Error: Download failed, no file found.")
                return
            
            temp_path = files[0]
            print(f"Downloaded to {temp_path}")
            
            # 2. Extract and Slice
            start_time = 90.0 
            slice_duration = 0.5 # Increased slightly
            
            if not os.path.exists('sounds'):
                os.makedirs('sounds')

            ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
            print(f"Using ffmpeg: {ffmpeg_path}")
            
            for i in range(1, 11):
                slice_start = start_time + ((i-1) * 0.5)
                output_file = f"sounds/animals-{i}.wav"
                
                # ffmpeg -y -ss <start> -t <duration> -i <input> <output>
                cmd = [
                    ffmpeg_path, '-y',
                    '-ss', str(slice_start),
                    '-t', str(slice_duration),
                    '-i', temp_path,
                    output_file,
                    '-loglevel', 'error'
                ]
                
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"Generated {output_file}")
                else:
                    print(f"Error generating {output_file}: {result.stderr}")
            
            # Cleanup
            if os.path.exists(temp_path):
                os.remove(temp_path)
                
            print("Done! Samples saved to sounds/animals-1.wav through animals-10.wav")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    download_and_process()
