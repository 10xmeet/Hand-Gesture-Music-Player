from flask import Flask, Response
import cv2
import mediapipe as mp
import pygame
import json

pygame.mixer.init(frequency=44100, channels=2)
pygame.mixer.set_num_channels(20)  # Allow many sounds simultaneously

# Load professional samples from StiickzZ remake
sample_base = 'sounds/The Chainsmokers & Coldplay - Something Just Like This (StiickzZ Remake)/'
sample_mapping = {
    'kick': sample_base + 'StiickzZ - Kick 27 E.wav',
    'clap': sample_base + 'StiickzZ - Clap 11.wav',
    'snap': sample_base + 'StiickzZ - Snap 02.wav',
    'crash': sample_base + 'StiickzZ - Crash 04.wav',
    'perc': sample_base + 'StiickzZ - Percussion 20.wav',
}

# Pre-load all samples
samples = {}
for i, (sample_name, sound_path) in enumerate(sample_mapping.items()):
    try:
        sound = pygame.mixer.Sound(sound_path)
        samples[sample_name] = sound
        print(f"Loaded {sample_name} from {sound_path}")
    except pygame.error as e:
        print(f"Could not load {sound_path}: {e}")

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Initialize the camera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Global state
current_state = {
    "volume": 0.5,
    "finger_count": 0,
    "gesture_name": "None",
    "active_samples": []
}

app = Flask(__name__)

@app.route('/status')
def status():
    return json.dumps(current_state)

@app.route('/video_feed')
def video_feed():
    def generate():
        global current_state
        prev_active_fingers = set()
        
        with mp_hands.Hands(
            model_complexity=0,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as hands:
            while True:
                success, image = cap.read()
                if not success:
                    print("Ignoring empty camera frame.")
                    break

                image.flags.writeable = False
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                results = hands.process(image)
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                current_active_fingers = set()
                volume = 0.5
                total_finger_count = 0

                if results.multi_hand_landmarks:
                    for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                        hand_label = handedness.classification[0].label
                        
                        # Calculate volume from wrist height
                        wrist_y = hand_landmarks.landmark[0].y
                        volume = max(0.0, min(1.0, 1 - wrist_y))

                        # Finger IDs: Left (1-5), Right (6-10)
                        offset = 0 if hand_label == "Left" else 5
                        
                        # Thumb
                        thumb_tip = hand_landmarks.landmark[4]
                        thumb_ip = hand_landmarks.landmark[3]
                        is_thumb_up = False
                        if hand_label == "Left":
                            if thumb_tip.x > thumb_ip.x: is_thumb_up = True
                        else:
                            if thumb_tip.x < thumb_ip.x: is_thumb_up = True
                        
                        if is_thumb_up: current_active_fingers.add(1 + offset)

                        # Other fingers (y-axis check)
                        tips = [8, 12, 16, 20]
                        pips = [6, 10, 14, 18]
                        
                        for i in range(4):
                            if hand_landmarks.landmark[tips[i]].y < hand_landmarks.landmark[pips[i]].y:
                                current_active_fingers.add(2 + i + offset)

                        # Draw landmarks
                        mp_drawing.draw_landmarks(
                            image,
                            hand_landmarks,
                            mp_hands.HAND_CONNECTIONS,
                            mp_drawing.DrawingSpec(color=(0, 255, 255), thickness=2, circle_radius=4),
                            mp_drawing.DrawingSpec(color=(255, 0, 255), thickness=2)
                        )

                total_finger_count = len(current_active_fingers)

                # Trigger samples on Rising Edge (Finger went from Down -> Up)
                # Map fingers to samples
                finger_to_sample = {
                    1: 'kick',    # Left thumb
                    2: 'clap',    # Left index
                    3: 'snap',    # Left middle
                    4: 'crash',   # Left ring
                    5: 'perc',    # Left pinky
                    6: 'kick',    # Right thumb
                    7: 'clap',    # Right index
                    8: 'snap',    # Right middle
                    9: 'crash',   # Right ring
                    10: 'perc'    # Right pinky
                }
                
                active_sample_names = []
                for finger_id in current_active_fingers:
                    if finger_id not in prev_active_fingers:
                        sample_name = finger_to_sample.get(finger_id)
                        if sample_name and sample_name in samples:
                            sound = samples[sample_name]
                            sound.set_volume(volume)
                            sound.play()
                            active_sample_names.append(sample_name)
                
                prev_active_fingers = current_active_fingers.copy()
                
                # Update global state
                current_state["volume"] = volume
                current_state["finger_count"] = total_finger_count
                current_state["gesture_name"] = "Playing" if total_finger_count > 0 else "Idle"
                current_state["active_samples"] = active_sample_names

                _, buffer = cv2.imencode('.jpg', image)
                frame = buffer.tobytes()

                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
