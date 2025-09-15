# gesture_mapping/mapper.py

def map_gesture_to_action(gesture):
    """
    Maps detected gestures to predefined Spotify control actions.
    """
    gesture_action_map = {
        "OPEN_PALM": "PLAY",
        "TWO_FINGERS": "PAUSE",
        "SWIPE_LEFT": "NEXT_TRACK",
        "SWIPE_RIGHT": "PREVIOUS_TRACK",
    }

    action = gesture_action_map.get(gesture, "NO_ACTION")
    print(f"[INFO] Gesture: {gesture} ➡️ Action: {action}")
    return action


# For independent testing of this module
if __name__ == "__main__":
    test_gestures = [
        "OPEN_PALM", "TWO_FINGERS", "SWIPE_LEFT", "SWIPE_RIGHT",
        "UNKNOWN", "NO_HAND"
    ]

    for gesture in test_gestures:
        action = map_gesture_to_action(gesture)
        print(f"Gesture: {gesture} → Action: {action}")
