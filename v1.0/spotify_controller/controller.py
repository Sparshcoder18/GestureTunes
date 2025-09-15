# spotify_controller/controller.py

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os

# Load credentials from .env file
load_dotenv()

class SpotifyController:
    def __init__(self):
        try:
            self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
                client_id=os.getenv("SPOTIPY_CLIENT_ID"),
                client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
                redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
                scope="user-read-playback-state,user-modify-playback-state"
            ))
            print("[INIT] ✅ Spotify client initialized.")
        except Exception as e:
            print(f"[ERROR] ❌ Failed to initialize Spotify client: {e}")

    def play(self):
        """
        Starts playback on the current active device.
        If no context exists, it will resume last played.
        """
        try:
            playback = self.sp.current_playback()
            if not playback or not playback.get('is_playing'):
                self.sp.start_playback()
                print("[SPOTIFY] ▶️ Playback started.")
            else:
                print("[SPOTIFY] ▶️ Already playing.")
        except Exception as e:
            print(f"[ERROR] ❌ Play failed: {e}")

    def pause(self):
        """
        Pauses playback on the current active device.
        """
        try:
            playback = self.sp.current_playback()
            if playback and playback.get('is_playing'):
                self.sp.pause_playback()
                print("[SPOTIFY] ⏸️ Playback paused.")
            else:
                print("[SPOTIFY] ⏹️ Nothing is currently playing.")
        except Exception as e:
            print(f"[ERROR] ❌ Pause failed: {e}")

    def next_track(self):
        """
        Skips to the next track.
        """
        try:
            self.sp.next_track()
            print("[SPOTIFY] ⏭️ Next track.")
        except Exception as e:
            print(f"[ERROR] ❌ Next track failed: {e}")

    def previous_track(self):
        """
        Goes to the previous track.
        """
        try:
            self.sp.previous_track()
            print("[SPOTIFY] ⏮️ Previous track.")
        except Exception as e:
            print(f"[ERROR] ❌ Previous track failed: {e}")

    def handle_action(self, action):
        """
        Receives action strings from mapper and runs appropriate Spotify commands.
        """
        print(f"[INFO] 🎬 Performing action: {action}")

        if action == "PLAY":
            self.play()
        elif action == "PAUSE":
            self.pause()
        elif action == "NEXT_TRACK":
            self.next_track()
        elif action == "PREVIOUS_TRACK":
            self.previous_track()
        else:
            print(f"[INFO] ⚠️ No action performed for: {action}")

    def get_current_playing(self):
        playback = self.sp.current_playback()
        if playback and playback.get("item"):
            return {
                "track": playback["item"]["name"],
                "artist": playback["item"]["artists"][0]["name"],
                "is_playing": playback["is_playing"]
            }
        return None


# Optional testing
if __name__ == "__main__":
    controller = SpotifyController()
    controller.play()
