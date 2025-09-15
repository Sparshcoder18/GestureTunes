# gesture_detection/detector.py

import cv2
import mediapipe as mp
import time
from config import SWIPE_COOLDOWN
from utils.helpers import is_cooldown_elapsed

DEBUG = False

def debug_print(msg):
    if DEBUG:
        print(msg)


class GestureDetector:
    def __init__(self, max_num_hands=2, detection_confidence=0.75, tracking_confidence=0.75):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=max_num_hands,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.prev_time = time.time()
        self.last_swipe_time = 0
        self.gesture = "NO_HAND"
        self.prev_positions = []

    def detect(self, frame):
        # Convert to RGB for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        gesture = self.extract_gesture(results, frame)
        return gesture

    def extract_gesture(self, results, frame):
        self.gesture = "NO_HAND"

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                fingers_up = self.count_fingers(hand_landmarks, frame)

                cx = int(hand_landmarks.landmark[0].x * frame.shape[1])
                cy = int(hand_landmarks.landmark[0].y * frame.shape[0])
                current_time = time.time()

                self.prev_positions.append((cx, cy, current_time))
                if len(self.prev_positions) > 10:
                    self.prev_positions.pop(0)

                dx = self.prev_positions[-1][0] - self.prev_positions[0][0]

                # Gesture classification
                if fingers_up == 5:
                    self.gesture = "OPEN_PALM"
                elif fingers_up == 2:
                    self.gesture = "TWO_FINGERS"
                elif abs(dx) > 80:
                    if is_cooldown_elapsed(self.last_swipe_time, SWIPE_COOLDOWN):
                        self.gesture = "SWIPE_RIGHT" if dx > 0 else "SWIPE_LEFT"
                        self.last_swipe_time = current_time
                    else:
                        self.gesture = "NO_ACTION"
                else:
                    self.gesture = "NO_HAND"

                # self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
        else:
            self.prev_positions.clear()

        debug_print(f"[GESTURE] Detected: {self.gesture}")
        return self.gesture

    def count_fingers(self, hand_landmarks, frame):
        fingers = []
        tip_ids = [4, 8, 12, 16, 20]
        landmarks = hand_landmarks.landmark

        # Thumb
        fingers.append(1 if landmarks[tip_ids[0]].x < landmarks[tip_ids[0] - 1].x else 0)

        # Other fingers
        for i in range(1, 5):
            fingers.append(1 if landmarks[tip_ids[i]].y < landmarks[tip_ids[i] - 2].y else 0)

        debug_print(f"[DEBUG] Fingers up: {sum(fingers)}")
        return sum(fingers)
