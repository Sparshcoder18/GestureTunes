# app.py

import cv2
import time

from gesture_detection.detector import GestureDetector
from gesture_mapping.mapper import map_gesture_to_action
from spotify_controller.controller import SpotifyController
from utils.helpers import is_cooldown_elapsed, log_gesture
from config import SWIPE_COOLDOWN
from gui.overlay import OverlayRenderer 


class GestureTunesApp:
    def __init__(self):
        self.detector = GestureDetector()
        self.controller = SpotifyController()
        self.overlay = OverlayRenderer()
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.last_action_time = 0
        print("[INFO] 🎵 GestureTunes initialized. Press 'q' to quit.")

    def run(self):
        frame_count = 0

        while self.cap.isOpened():
            frame_count += 1
            if frame_count % 2 == 0:  # ✅ Only every second frame
                gesture = self.detector.detect(frame)

            success, frame = self.cap.read()
            if not success:
                print("[ERROR] ❌ Failed to grab frame.")
                break

            frame = cv2.resize(frame, (640, 480))  # Consistent resolution

            # 1. Detect gesture
            gesture = self.detector.detect(frame)

            # 2. Show FPS + gesture label
            self.overlay.draw_fps(frame)
            self.overlay.draw_gesture_label(frame, gesture)

            # 3. Action handling
            current_time = time.time()
            action = map_gesture_to_action(gesture)

            if gesture in ["SWIPE_LEFT", "SWIPE_RIGHT"]:
                if not is_cooldown_elapsed(self.last_action_time, SWIPE_COOLDOWN):
                    self.overlay.draw_cooldown(frame)
                else:
                    self.controller.handle_action(action)
                    self.last_action_time = current_time
            else:
                self.controller.handle_action(action)

            # 4. Track info
            track_info = self.controller.get_current_playing()
            if track_info:
                self.overlay.draw_track_info(frame, track_info)

            # 5. Show everything
            cv2.imshow("GestureTunes", frame)

            # 6. Quit app
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            # 7. Gesture Logs
            action = map_gesture_to_action(gesture)
            log_gesture(gesture, action)  # ✅ log each gesture-action pair


        self.cap.release()
        cv2.destroyAllWindows()
        print("[INFO] 👋 Application closed.")

if __name__ == "__main__":
    app = GestureTunesApp()
    app.run()
