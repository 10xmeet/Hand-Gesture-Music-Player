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
    6: "sounds/tom-3.mp3",
    7: "sounds/cr78-Cymbal.mp3",
    8: "sounds/cr78-Guiro 1.mp3",
    9: "sounds/tempest-HiHat Metal.mp3",
    10: "sounds/cr78-Bongo High.mp3"
}

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)
# Set higher resolution and window size
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # Set width to 1280 pixels
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)   # Set height to 720 pixels

# Ensure the window is resized to match the resolution
cv2.namedWindow('MediaPipe Hands', cv2.WINDOW_NORMAL)
cv2.resizeWindow('MediaPipe Hands', 1280, 720)
with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        fingerCount = 0
        volume = 0.5  # Default volume

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

                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())

        # Enhanced and modernized display customization
        # Function to display modern and fixed UI elements
        def display_custom_ui(image, volume, finger_count, gesture_name="Unknown", prev_volume=0):
            overlay = image.copy()
            height, width, _ = image.shape
        
            # Semi-transparent background for UI
            cv2.rectangle(overlay, (10, height - 150), (width - 10, height - 10), (0, 0, 0), -1)
            alpha = 0.6  # Transparency factor
            cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0, image)
        
            # Fixed and improved volume bar
            bar_x_start = 20
            bar_y_start = height - 120
            bar_width = 250
            bar_height = 20
        
            # Smooth animation for volume bar
            animated_volume = prev_volume + (volume - prev_volume) * 0.1
        
            # Draw volume bar background
            cv2.rectangle(image, (bar_x_start, bar_y_start), (bar_x_start + bar_width, bar_y_start + bar_height), (50, 50, 50), -1)
        
            # Draw volume bar foreground
            cv2.rectangle(image, (bar_x_start, bar_y_start), (bar_x_start + int(animated_volume * bar_width), bar_y_start + bar_height), (0, 255, 0), -1)
        
            # Volume text
            cv2.putText(image, f"Volume: {volume:.2f}", (bar_x_start, bar_y_start - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
            # Finger count
            cv2.putText(image, f"Fingers: {finger_count}", (bar_x_start, height - 70), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
        
            # Gesture name
            cv2.putText(image, f"Gesture: {gesture_name}", (bar_x_start, height - 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        
            return animated_volume
        
        # Fix sound playback logic with delay
        # Multi-Track Playback Logic
        # Allow multiple sounds to play simultaneously using pygame.mixer.Sound
        multi_track_sounds = {}
        for key, sound_path in sounds_mapping.items():
            multi_track_sounds[key] = pygame.mixer.Sound(sound_path)
        
        # Play multiple tracks based on finger count
        if fingerCount in multi_track_sounds:
            sound = multi_track_sounds[fingerCount]
            sound.set_volume(volume)  # Set volume dynamically
            sound.play()
            pygame.time.delay(500)  # Add a 500ms delay to playback
        
        # Replace the existing display logic with the fixed function
        prev_volume = 0  # Initialize previous volume for animation
        prev_volume = display_custom_ui(image, volume, fingerCount, "Custom Gesture", prev_volume)
        cv2.putText(image, f"Volume: {volume:.2f}", (50, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(image, str(fingerCount), (50, 450), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 0), 10)
        cv2.imshow('MediaPipe Hands', image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()

# Load user-defined sound mappings if available
try:
    with open("user_sound_mapping.json", "r") as f:
        user_sounds_mapping = json.load(f)
        sounds_mapping.update(user_sounds_mapping)
except FileNotFoundError:
    print("No user-defined sound mappings found. Using default mappings.")

# Function to save user-defined sound mappings
def save_user_sound_mapping(new_mapping):
    with open("user_sound_mapping.json", "w") as f:
        json.dump(new_mapping, f)

# Example: Adding a new mapping dynamically (this can be replaced with a UI or input logic)
# Uncomment the following lines to test adding a new mapping
# new_mapping = {11: "sounds/new-sound.mp3"}
# sounds_mapping.update(new_mapping)
# save_user_sound_mapping(sounds_mapping)

# Gesture Training Mode
# Function to train custom gestures
def train_custom_gesture():
    print("Gesture Training Mode: Perform a gesture and press 's' to save it.")
    trained_gestures = {}

    while True:
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style()
                )

        cv2.imshow('Gesture Training', image)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):
            # Save the gesture landmarks
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    landmarks = [
                        [lm.x, lm.y, lm.z] for lm in hand_landmarks.landmark
                    ]
                    gesture_name = input("Enter a name for this gesture: ")
                    trained_gestures[gesture_name] = landmarks

            print("Gesture saved! Press 'q' to quit training mode.")

        elif key == ord('q'):
            # Save trained gestures to a file
            with open("trained_gestures.json", "w") as f:
                json.dump(trained_gestures, f)
            print("Training mode exited. Gestures saved.")
            break

    cv2.destroyWindow('Gesture Training')

# Uncomment the following line to activate training mode
# train_custom_gesture()
