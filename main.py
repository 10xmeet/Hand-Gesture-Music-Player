from flask import Flask, Response
import cv2
import mediapipe as mp
import pygame
import json

pygame.mixer.init(frequency=44100, channels=2)
pygame.mixer.set_num_channels(10)  # Allow multiple sounds simultaneously

# Load the 4 main stem loops (we'll use 4 of the animals samples as "stems")
stem_mapping = {
    'drums': 'sounds/animals-1.wav',    # Thumb controls drums
    'bass': 'sounds/animals-2.wav',      # Index controls bass
    'melody': 'sounds/animals-3.wav',    # Middle controls melody
    'vocals': 'sounds/animals-4.wav'     # Ring controls vocals
}

# Pre-load and start all stems playing in loops
stems = {}
for i, (stem_name, sound_path) in enumerate(stem_mapping.items()):
    try:
        sound = pygame.mixer.Sound(sound_path)
        channel = pygame.mixer.Channel(i)
        channel.play(sound, loops=-1)  # Loop indefinitely
        channel.set_volume(0.0)  # Start muted
        stems[stem_name] = {'sound': sound, 'channel': channel}
        print(f"Loaded {stem_name} from {sound_path}")
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
    "active_stems": []
}

app = Flask(__name__)

@app.route('/status')
def status():
    return json.dumps(current_state)

@app.route('/video_feed')
def video_feed():
    def generate():
        global current_state
        
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

                active_fingers = {
                    'drums': False,
                    'bass': False,
                    'melody': False,
                    'vocals': False
                }
                volume = 0.5
                total_finger_count = 0

                if results.multi_hand_landmarks:
                    for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                        hand_label = handedness.classification[0].label
                        
                        # Calculate volume from wrist height
                        wrist_y = hand_landmarks.landmark[0].y
                        volume = max(0.0, min(1.0, 1 - wrist_y))

                        # Check which fingers are up
                        # Thumb
                        thumb_tip = hand_landmarks.landmark[4]
                        thumb_ip = hand_landmarks.landmark[3]
                        is_thumb_up = False
                        if hand_label == "Left":
                            if thumb_tip.x > thumb_ip.x: is_thumb_up = True
                        else:
                            if thumb_tip.x < thumb_ip.x: is_thumb_up = True
                        
                        if is_thumb_up: 
                            active_fingers['drums'] = True
                            total_finger_count += 1

                        # Index -> Bass
                        if hand_landmarks.landmark[8].y < hand_landmarks.landmark[6].y:
                            active_fingers['bass'] = True
                            total_finger_count += 1
                        
                        # Middle -> Melody
                        if hand_landmarks.landmark[12].y < hand_landmarks.landmark[10].y:
                            active_fingers['melody'] = True
                            total_finger_count += 1
                        
                        # Ring -> Vocals
                        if hand_landmarks.landmark[16].y < hand_landmarks.landmark[14].y:
                            active_fingers['vocals'] = True
                            total_finger_count += 1

                        # Draw landmarks
                        mp_drawing.draw_landmarks(
                            image,
                            hand_landmarks,
                            mp_hands.HAND_CONNECTIONS,
                            mp_drawing.DrawingSpec(color=(0, 255, 255), thickness=2, circle_radius=4),
                            mp_drawing.DrawingSpec(color=(255, 0, 255), thickness=2)
                        )

                # Update stem volumes based on active fingers
                active_stem_names = []
                for stem_name, is_active in active_fingers.items():
                    if stem_name in stems:
                        target_volume = volume if is_active else 0.0
                        stems[stem_name]['channel'].set_volume(target_volume)
                        if is_active:
                            active_stem_names.append(stem_name)
                
                # Update global state
                current_state["volume"] = volume
                current_state["finger_count"] = total_finger_count
                current_state["gesture_name"] = "Mixing" if total_finger_count > 0 else "Idle"
                current_state["active_stems"] = active_stem_names

                _, buffer = cv2.imencode('.jpg', image)
                frame = buffer.tobytes()

                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
