
import os
import sys

# Check Assets
assets_dir = r"c:\Users\rathu\OneDrive\Documents\Assitant\desktop_assistant\assets"
required_assets = ["idle.png", "thinking.png", "dancing.gif"]
missing = []

print("Checking Assets...")
for asset in required_assets:
    path = os.path.join(assets_dir, asset)
    if os.path.exists(path):
        print(f"[OK] Found {asset}")
    else:
        print(f"[FAIL] Missing {asset}")
        missing.append(asset)

# Check Code Logic
print("\nChecking Code Logic...")
try:
    with open(r"c:\Users\rathu\OneDrive\Documents\Assitant\desktop_assistant\modules\gui.py", "r") as f:
        gui_content = f.read()
        if "self.thinking_movie = QMovie(Config.THINKING_IMAGE)" in gui_content:
            print("[OK] gui.py loads thinking image")
        else:
            print("[FAIL] gui.py missing thinking image load")
            
        if 'elif state == "thinking":' in gui_content:
            print("[OK] gui.py handles thinking state")
        else:
            print("[FAIL] gui.py missing thinking state handler")

    with open(r"c:\Users\rathu\OneDrive\Documents\Assitant\desktop_assistant\main.py", "r") as f:
        main_content = f.read()
        if 'self.state_changed.emit("thinking")' in main_content:
            print("[OK] main.py emits thinking state")
        else:
            print("[FAIL] main.py missing thinking state emit")

except Exception as e:
    print(f"[ERROR] Could not read files: {e}")

if not missing:
    print("\nVerification Passed!")
else:
    print("\nVerification Failed!")
