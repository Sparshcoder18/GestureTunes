# 🎵 GestureTunes v1.0

Control Spotify using your hand gestures via webcam in real-time 🤚🎶  
Built with Python, OpenCV, MediaPipe, and Spotipy.

---

## 🚀 Features

- ✋ Open Palm → **Play**
- ✌️ Two Fingers → **Pause**
- 👈 Swipe Left → **Next Track**
- 👉 Swipe Right → **Previous Track**
- 🖥️ Overlay GUI: FPS, Track Info, Gesture Name
- 📝 Gesture logging with timestamp

---

## 🧰 Tech Stack

- Python 3.10
- OpenCV
- MediaPipe
- Spotipy
- Dotenv

---

## 🔧 Setup

```bash
git clone https://github.com/yourusername/GestureTunes.git
cd GestureTunes

python -m venv gesture-env
gesture-env\Scripts\activate    # On Windows

pip install -r requirements.txt

# Add .env file with your Spotify credentials
touch .env
# Add:
# SPOTIPY_CLIENT_ID=your_client_id
# SPOTIPY_CLIENT_SECRET=your_client_secret
# SPOTIPY_REDIRECT_URI=http://localhost:8888/callback

python app.py
