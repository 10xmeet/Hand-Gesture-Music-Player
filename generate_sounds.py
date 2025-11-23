import wave
import math
import struct
import random
import os

def save_wav(filename, data, sample_rate=44100):
    with wave.open(filename, 'w') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sample_rate)
        for sample in data:
            # Clamp to 16-bit range
            sample = max(-32768, min(32767, int(sample)))
            w.writeframes(struct.pack('<h', sample))
    print(f"Generated {filename}")

def generate_kick(duration=0.3, sample_rate=44100):
    data = []
    num_samples = int(duration * sample_rate)
    for i in range(num_samples):
        t = i / sample_rate
        # Frequency drop for kick
        freq = 150 * math.exp(-20 * t)
        amp = 32000 * math.exp(-10 * t)
        sample = amp * math.sin(2 * math.pi * freq * t)
        data.append(sample)
    return data

def generate_snare(duration=0.2, sample_rate=44100):
    data = []
    num_samples = int(duration * sample_rate)
    for i in range(num_samples):
        t = i / sample_rate
        # Noise + Tone
        noise = random.uniform(-1, 1)
        tone = math.sin(2 * math.pi * 200 * t)
        amp = 30000 * math.exp(-15 * t)
        sample = amp * (0.8 * noise + 0.2 * tone)
        data.append(sample)
    return data

def generate_bass(duration=0.5, sample_rate=44100, freq=55): # A1
    data = []
    num_samples = int(duration * sample_rate)
    for i in range(num_samples):
        t = i / sample_rate
        # Sawtooth-ish
        sample = 0
        for h in range(1, 5):
            sample += (1/h) * math.sin(2 * math.pi * freq * h * t)
        
        amp = 25000 * math.exp(-2 * t)
        # Low pass filter effect (simple approximation by reducing higher harmonics over time - already done slightly by exp decay)
        data.append(sample * amp)
    return data

def generate_lead(duration=0.5, sample_rate=44100, freq=440): # A4
    data = []
    num_samples = int(duration * sample_rate)
    for i in range(num_samples):
        t = i / sample_rate
        # Square wave ish
        val = math.sin(2 * math.pi * freq * t)
        val = 1 if val > 0 else -1
        
        amp = 20000 * math.exp(-4 * t)
        data.append(val * amp)
    return data

def generate_pluck(duration=0.5, sample_rate=44100, freq=660): # E5
    data = []
    num_samples = int(duration * sample_rate)
    # Karplus-Strong simplified (just decaying sine with some noise burst at start)
    for i in range(num_samples):
        t = i / sample_rate
        sample = math.sin(2 * math.pi * freq * t)
        amp = 28000 * math.exp(-8 * t)
        data.append(sample * amp)
    return data

def main():
    if not os.path.exists('sounds'):
        os.makedirs('sounds')
        
    save_wav('sounds/edm-kick.wav', generate_kick())
    save_wav('sounds/edm-snare.wav', generate_snare())
    save_wav('sounds/edm-bass.wav', generate_bass())
    save_wav('sounds/edm-lead.wav', generate_lead())
    save_wav('sounds/edm-pluck.wav', generate_pluck())

if __name__ == "__main__":
    main()
