from flask import Flask, Response
import cv2
import mediapipe as mp
import pygame
import json

pygame.mixer.init()

sounds_mapping = {
    1: "sounds/animals-1.wav",
    2: "sounds/animals-2.wav",
    3: "sounds/animals-3.wav",
    4: "sounds/animals-4.wav",
    5: "sounds/animals-5.wav",
    6: "sounds/animals-6.wav",
    7: "sounds/animals-7.wav",
    8: "sounds/animals-8.wav",
    9: "sounds/animals-9.wav",
    10: "sounds/animals-10.wav"
}

# ... (Load user mappings - kept same) ...

# Pre-load sounds
multi_track_sounds = {}
for i in range(1, 11):
    if i in sounds_mapping:
        sound_path = sounds_mapping[i]
        try:
            multi_track_sounds[i] = pygame.mixer.Sound(sound_path)
        except pygame.error as e:
            print(f"Could not load sound {sound_path}: {e}")

app = Flask(__name__)

@app.route('/status')
def status():
    return json.dumps(current_state)

@app.route('/video_feed')
def video_feed():
    def generate():
        global current_state
        prev_active_fingers = set() # Track which fingers were up in the last frame
        
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
                        hand_label = handedness.classification[0].label # "Left" or "Right"
                        
                        # Calculate volume from wrist height (using first hand found for simplicity)
                        wrist_y = hand_landmarks.landmark[0].y
                        volume = max(0.0, min(1.0, 1 - wrist_y))

                        # Finger IDs: Left (1-5), Right (6-10)
                        # Thumb, Index, Middle, Ring, Pinky
                        offset = 0 if hand_label == "Left" else 5
                        
                        # Landmarks
                        # Thumb: 4 vs 3 (x-axis check depends on hand)
                        thumb_tip = hand_landmarks.landmark[4]
                        thumb_ip = hand_landmarks.landmark[3]
                        
                        is_thumb_up = False
                        if hand_label == "Left":
                            if thumb_tip.x > thumb_ip.x: is_thumb_up = True
                        else:
                            if thumb_tip.x < thumb_ip.x: is_thumb_up = True
                        
                        if is_thumb_up: current_active_fingers.add(1 + offset)

                        # Other fingers (y-axis check)
                        # Index (8 vs 6), Middle (12 vs 10), Ring (16 vs 14), Pinky (20 vs 18)
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

                # Trigger sounds on Rising Edge (Finger went from Down -> Up)
                for finger_id in current_active_fingers:
                    if finger_id not in prev_active_fingers:
                        if finger_id in multi_track_sounds:
                            sound = multi_track_sounds[finger_id]
                            sound.set_volume(volume)
                            sound.play()
                
                prev_active_fingers = current_active_fingers.copy()
                
                # Update global state
                current_state["volume"] = volume
                current_state["finger_count"] = total_finger_count
                current_state["gesture_name"] = "Polyphonic" if total_finger_count > 0 else "Idle"

                _, buffer = cv2.imencode('.jpg', image)
                frame = buffer.tobytes()

                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
