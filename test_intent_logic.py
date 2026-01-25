
def quick_intent_check(text):
    text = text.lower()
    
    # Music Controls
    if "play" in text:
        query = text.replace("play", "").replace("music", "").strip()
        return "play_music", query
    elif "pause" in text or "stop music" in text: 
        return "stop_music", ""
    elif "next" in text or "skip" in text:
        return "next_track", ""
    elif "queue" in text and "add" in text:
        query = text.replace("add", "").replace("to", "").replace("queue", "").strip()
        return "add_to_queue", query
        
    # System Controls
    elif "open" in text:
        query = text.replace("open", "").strip()
        return "open_app", query
    elif "volume" in text:
        query = text.replace("set", "").replace("volume", "").replace("to", "").strip()
        return "set_volume", query
    elif "brightness" in text:
        query = text.replace("set", "").replace("brightness", "").replace("to", "").strip()
        return "set_brightness", query
    elif "battery" in text or "system info" in text:
        return "system_info", ""
    elif "screenshot" in text:
        return "take_screenshot", ""
        
    return None, None

test_cases = [
    ("play music", "play_music"),
    ("open notepad", "open_app"),
    ("stop music", "stop_music"),
    ("next song", "next_track"),
    ("add believer to queue", "add_to_queue"),
    ("set volume to 50", "set_volume"),
    ("tell me a joke", None)
]

print("Running Intent Tests...")
failed = False
for text, expected in test_cases:
    intent, query = quick_intent_check(text)
    if intent != expected:
        print(f"FAIL: '{text}' -> Got {intent}, Expected {expected}")
        failed = True
    else:
        print(f"PASS: '{text}' -> {intent}")

if not failed:
    print("All tests passed!")
else:
    print("Some tests failed.")
