# gui/overlay.py

import cv2
import time

class OverlayRenderer:
    def __init__(self):
        self.prev_time = time.time()

    def draw_fps(self, frame):
        """
        Display the current Frames Per Second (FPS) on the frame.
        """
        current_time = time.time()
        fps = int(1 / (current_time - self.prev_time))
        self.prev_time = current_time

        cv2.putText(frame, f"FPS: {fps}", (10, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    def draw_gesture_label(self, frame, gesture):
        """
        Displays the currently detected gesture on the frame.
        """
        cv2.putText(frame, f"Gesture: {gesture}", (10, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

    def draw_cooldown(self, frame):
        """
        Shows a "Cooldown..." message to indicate action throttling.
        """
        cv2.putText(frame, "Cooldown...", (10, 460),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    def draw_track_info(self, frame, track_info):
        """
        Display currently playing track and artist info.
        """
        text = f"{track_info['track']} - {track_info['artist']}"
        color = (0, 255, 0) if track_info['is_playing'] else (0, 0, 255)

        cv2.putText(frame, text, (10, 420),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
