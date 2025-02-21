import pyautogui
import time

levels = {
    "pits": {
        "1": [
            ("keyDown", "right"),
            2,
            "up",
            1,
            ("keyup", "right"),
            3,
            ("keyDown", "right"),
            2,
            "up",
            0.4,
            "up",
            1,
            ("keyup", "right"),
            3,
            ("keyDown", "right"),
            1,
            "up",
            1,
            ("keyup", "right"),
            3,
            ("keyDown", "right"),
            "up",
            3,
            ("keyup", "right"),
            3,
            ("keyDown", "right"),
            2.8,
            "up",
            0.5,
            ("keyup", "right"),
            3,
            ("keyDown", "space"),
            ("keyUp", "space"),
            # 5 always delay
            5, 
            ("keyDown", "right"),
            0.45,
            ("keyup", "right"),
            ("keyDown", "left"),
            "up",
            1.2,
            "up",
            ("keyup", "right"),
            3,
            ("keyDown", "right"),
            0.5,
            "up",
            1,
            "up",
            1.4,
            "up",
            ("keyup", "right"),
            3,
            ("keyDown", "right"),
            0.1,
            ("keyUp", "right"),
            1.5,
            "up",
            ("keyDown", "right"),
            ("keyup", "right"),
            3,
            ("keyDown", "right"),
            2.3,
            "up",
            0.3,
            "up",
            0.3,
            "up",
            0.3,
            "up",
            0.3,
            "up",
            ("keyup", "right"),
            3,
            ("keyDown", "left"),
            1.5,
            ("KeyUp", "left"),
            ("keyDown", "right"),
            1.8,
            ("keyUp", "right"),
            0.6,
            ("keyDown", "left"),
            "up",
            ("keyup", "right"),
            3,
        ]
    }
}

# Manually select a level to use
door = input("Which door are you playing? (default: pits)") or "pits"
level = input("Which level are you playing? (default: 1)") or "1"
print("level", level)
timings = levels[door][level]

print("Move your focus to the window, you have 5 seconds!")
time.sleep(5)

pyautogui.press("right")
pyautogui.press("left")

# Loop over each item in this level
for thing in timings:
    print("step", thing)

    # If it's an integer or float, sleep that amount of time
    if isinstance(thing, int) or isinstance(thing, float):
        time.sleep(thing)

    # If it's a string, press that key
    elif isinstance(thing, str):
        pyautogui.press(thing)

    # If it's a tuple (), then take the first value as the action (like keyDown)
    # and the second value as the key
    elif isinstance(thing, tuple):
        if thing[0] == "keyDown":
            pyautogui.keyDown(thing[1])
        elif thing[0] == "keyUp":
            pyautogui.keyUp(thing[1])
        else:
            pyautogui.press(thing[1])
