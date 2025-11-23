from flask import Flask, Response
import cv2
import mediapipe as mp
import pygame
import json

pygame.mixer.init()

sounds_mapping = {
    1: "sounds/kick-bass.mp3",
    2: "sounds/crash.mp3",
    3: "sounds/snare.mp3",
    4: "sounds/tom-1.mp3",
    5: "sounds/tom-2.mp3",
    6: "sounds/edm-kick.wav",
    7: "sounds/edm-snare.wav",
    8: "sounds/edm-bass.wav",
    9: "sounds/edm-lead.wav",
    10: "sounds/edm-pluck.wav"
}

# Load user-defined sound mappings if available (before initializing mixer sounds)
try:
    with open("user_sound_mapping.json", "r") as f:
        user_sounds_mapping = json.load(f)
        sounds_mapping.update(user_sounds_mapping)
except FileNotFoundError:
    print("No user-defined sound mappings found. Using default mappings.")

multi_track_sounds = {}
for i in range(1, 11):
    if i in sounds_mapping:
        sound_path = sounds_mapping[i]
        try:
            multi_track_sounds[i] = pygame.mixer.Sound(sound_path)
        except pygame.error as e:
            print(f"Could not load sound {sound_path}: {e}")

def display_custom_ui(image, volume, finger_count, gesture_name, prev_volume):
    # Display volume bar
    bar_height = int(volume * 200)
    cv2.rectangle(image, (20, 250), (50, 250 - bar_height), (0, 255, 0), -1)
    cv2.putText(image, f"Vol: {int(volume * 100)}%", (10, 280), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    # Display finger count
    cv2.putText(image, f"Fingers: {finger_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # Display gesture name
    cv2.putText(image, f"Gesture: {gesture_name}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # Simple animation for volume change
    if abs(volume - prev_volume) > 0.05:
        cv2.putText(image, "Volume Change!", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    return volume

app = Flask(__name__)

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

# Initialize the camera
cap = cv2.VideoCapture(0)
# Set higher resolution for the camera input
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Global state to share between video loop and status endpoint
current_state = {
    "volume": 0.5,
    "finger_count": 0,
    "gesture_name": "None"
}

@app.route('/status')
def status():
    return json.dumps(current_state)

@app.route('/video_feed')
def video_feed():
    def generate():
        global current_state
        prev_volume = 0  # Initialize previous volume for animation
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

                fingerCount = 0
                volume = 0.5  # Default volume
                handLandmarks = [] # Initialize handLandmarks

                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        handIndex = results.multi_hand_landmarks.index(hand_landmarks)
                        handLabel = results.multi_handedness[handIndex].classification[0].label
                        handLandmarks = []

                        for landmarks in hand_landmarks.landmark:
                            handLandmarks.append([landmarks.x, landmarks.y])

                        # Count fingers logic
                        if handLabel == "Left" and handLandmarks[4][0] > handLandmarks[3][0]:
                            fingerCount = fingerCount + 1
                        elif handLabel == "Right" and handLandmarks[4][0] < handLandmarks[3][0]:
                            fingerCount = fingerCount + 1

                        if handLandmarks[8][1] < handLandmarks[6][1]:
                            fingerCount = fingerCount + 1
                        if handLandmarks[12][1] < handLandmarks[10][1]:
                            fingerCount = fingerCount + 1
                        if handLandmarks[16][1] < handLandmarks[14][1]:
                            fingerCount = fingerCount + 1
                        if handLandmarks[20][1] < handLandmarks[18][1]:
                            fingerCount = fingerCount + 1

                        # Calculate volume based on hand height (y-coordinate of wrist landmark)
                        wrist_y = handLandmarks[0][1]  # y-coordinate of wrist
                        volume = max(0.0, min(1.0, 1 - wrist_y))  # Normalize to range [0, 1]

                        # Explicitly set custom colors for hand landmarks and connections
                        # Using a more "Cyberpunk" color scheme (Neon Cyan and Pink)
                        mp_drawing.draw_landmarks(
                            image,
                            hand_landmarks,
                            mp_hands.HAND_CONNECTIONS,
                            mp_drawing.DrawingSpec(color=(0, 255, 255), thickness=2, circle_radius=4),  # Cyan for landmarks
                            mp_drawing.DrawingSpec(color=(255, 0, 255), thickness=2)  # Magenta for connections
                        )

                        # Play multiple tracks based on finger count
                        if fingerCount in multi_track_sounds:
                            sound = multi_track_sounds[fingerCount]
                            sound.set_volume(volume)  # Set volume dynamically
                            sound.play()
                
                # Update global state
                current_state["volume"] = volume
                current_state["finger_count"] = fingerCount
                current_state["gesture_name"] = "Active" if fingerCount > 0 else "None"

                _, buffer = cv2.imencode('.jpg', image)
                frame = buffer.tobytes()

                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
