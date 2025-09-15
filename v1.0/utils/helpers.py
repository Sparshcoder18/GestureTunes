# utils/helpers.py
import time
def log_gesture(gesture, action):
    """
    Logs the gesture and mapped action to a text file.
    """
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] Gesture: {gesture} ➡️ Action: {action}\n"

    # ✅ Force UTF-8 encoding to support emojis and symbols
    with open("logs/gestures_log.txt", "a", encoding="utf-8") as log_file:
        log_file.write(log_line)

def is_cooldown_elapsed(last_time, cooldown_seconds):
    """
    Checks whether the cooldown period has passed.
    """
    return time.time() - last_time >= cooldown_seconds

def rate_limit_action(action_timestamp_dict, gesture, cooldown_seconds):
    """
    Ensures rate-limiting of individual gesture actions.
    """
    current_time = time.time()
    last_time = action_timestamp_dict.get(gesture, 0)
    if current_time - last_time >= cooldown_seconds:
        action_timestamp_dict[gesture] = current_time
        return True
    return False
