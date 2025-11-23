import yt_dlp
import os
import imageio_ffmpeg
import subprocess
import shutil
import glob

def separate_audio():
    url = "https://www.youtube.com/watch?v=5gga8E43clk"
    
    # 1. Download
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'temp_animals_full.%(ext)s',
        'noplaylist': True,
        'quiet': True,
    }

    print(f"Downloading {url}...")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
            files = glob.glob("temp_animals_full.*")
            if not files:
                print("Error: Download failed.")
                return
            temp_path = files[0]
            
            # 2. Trim to 30s Loop (The Drop: 1:28 - 1:58)
            start_time = 88.0 
            duration = 30.0
            loop_path = "animals_loop.wav"
            
            ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
            print(f"Trimming audio using {ffmpeg_path}...")
            
            cmd = [
                ffmpeg_path, '-y',
                '-ss', str(start_time),
                '-t', str(duration),
                '-i', temp_path,
                loop_path,
                '-loglevel', 'error'
            ]
            subprocess.run(cmd, check=True)
            print(f"Trimmed to {loop_path}")
            
            # 3. Separate Stems using Demucs
            print("Separating stems (this may take a moment)...")
            # Run demucs as a subprocess
            # demucs -n htdemucs --two-stems=vocals -d cpu animals_loop.wav (No, we want 4 stems)
            # demucs -n htdemucs -d cpu animals_loop.wav
            cmd_demucs = ["demucs", "-n", "htdemucs", "-d", "cpu", loop_path]
            subprocess.run(cmd_demucs, check=True)
            
            # 4. Move files
            # Output is usually in separated/htdemucs/animals_loop/
            source_dir = os.path.join("separated", "htdemucs", "animals_loop")
            target_dir = os.path.join("sounds", "stems")
            
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)
                
            stems = ["drums.wav", "bass.wav", "other.wav", "vocals.wav"]
            for stem in stems:
                src = os.path.join(source_dir, stem)
                dst = os.path.join(target_dir, stem)
                if os.path.exists(src):
                    shutil.copy2(src, dst)
                    print(f"Moved {stem} to {target_dir}")
                else:
                    print(f"Warning: {stem} not found in output.")
            
            # Cleanup
            if os.path.exists(temp_path): os.remove(temp_path)
            if os.path.exists(loop_path): os.remove(loop_path)
            # Optional: remove separated folder? Maybe keep for cache.
            
            print("Done! Stems are ready in sounds/stems/")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    separate_audio()
