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
            sample = max(-32768, min(32767, int(sample)))
            w.writeframes(struct.pack('<h', sample))
    print(f"Generated {filename}")

def generate_kick(duration=0.4, sample_rate=44100):
    data = []
    num_samples = int(duration * sample_rate)
    for i in range(num_samples):
        t = i / sample_rate
        # Frequency sweep: 150Hz -> 50Hz
        freq = 150 * math.exp(-15 * t)
        # Amplitude envelope
        amp = 32000 * math.exp(-8 * t)
        # Add a "click" at the start
        click = 0
        if t < 0.01:
            click = random.uniform(-10000, 10000) * (1 - t/0.01)
        
        sample = amp * math.sin(2 * math.pi * freq * t) + click
        data.append(sample)
    return data

def generate_snare(duration=0.25, sample_rate=44100):
    data = []
    num_samples = int(duration * sample_rate)
    for i in range(num_samples):
        t = i / sample_rate
        # Tonal body: 200Hz
        tone = 15000 * math.exp(-15 * t) * math.sin(2 * math.pi * 200 * t)
        # Noise wash
        noise_amp = 20000 * math.exp(-10 * t)
        noise = noise_amp * random.uniform(-1, 1)
        
        data.append(tone + noise)
    return data

def generate_bass(duration=0.6, sample_rate=44100, freq=55): # A1
    data = []
    num_samples = int(duration * sample_rate)
    for i in range(num_samples):
        t = i / sample_rate
        # 3 Detuned Sawtooth waves for "Fat" sound
        saw1 = (2 * ((freq * t) % 1) - 1)
        saw2 = (2 * ((freq * 1.01 * t) % 1) - 1)
        saw3 = (2 * ((freq * 0.99 * t) % 1) - 1)
        
        mix = (saw1 + saw2 + saw3) / 3
        
        # Low pass filter simulation (reduce high freq over time)
        # Simple amplitude envelope
        amp = 28000 * min(1.0, t * 100) * math.exp(-3 * t) # Attack and decay
        
        data.append(mix * amp)
    return data

def generate_lead(duration=0.8, sample_rate=44100, freq=440): # A4
    data = []
    num_samples = int(duration * sample_rate)
    for i in range(num_samples):
        t = i / sample_rate
        # Square wave with vibrato
        vibrato = 5 * math.sin(2 * math.pi * 6 * t)
        f = freq + vibrato
        
        square = 1 if math.sin(2 * math.pi * f * t) > 0 else -1
        
        # Add some delay/echo
        delay_sample = 0
        delay_time = 0.2
        delay_idx = i - int(delay_time * sample_rate)
        if delay_idx >= 0 and delay_idx < len(data):
            delay_sample = data[delay_idx] * 0.4
            
        amp = 20000 * min(1.0, t * 50) * math.exp(-2 * t)
        
        sample = (square * amp) + delay_sample
        data.append(sample)
    return data

def generate_pluck(duration=1.0, sample_rate=44100, freq=660): # E5
    data = []
    num_samples = int(duration * sample_rate)
    # Karplus-Strong Algorithm
    buffer_len = int(sample_rate / freq)
    buffer = [random.uniform(-1, 1) for _ in range(buffer_len)]
    
    current_sample = 0
    for i in range(num_samples):
        # Average of current and previous sample (Low pass)
        new_val = 0.5 * (buffer[i % buffer_len] + buffer[(i - 1) % buffer_len])
        # Decay
        new_val *= 0.994
        buffer[i % buffer_len] = new_val
        
        amp = 30000
        data.append(new_val * amp)
        
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
