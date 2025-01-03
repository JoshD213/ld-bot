import pyautogui
import time
import os

levels = {
    "pits": {
        "1": [("keyDown", "right"), 2, "up"],
        "2": [("keyDown", "right"), 2, "up", 0.4, "up"],
        "3": [("keyDown", "right"), 1, "up"],
        "4": [
            ("keyDown", "right"),
            "up",
        ],
        "5": [("keyDown", "right"), 2.8, "up"],
    },
    "spikes": {
        "1": [
            ("keyDown", "right"),
            0.45,
            ("keyUp", "right"),
            0.01,
            ("keyDown", "left"),
            "up",
            1.2,
            "up",
        ],
        "2": [("keyDown", "right"), 0.5, "up", 1, "up", 1.4, "up"],
        "3": [
            ("keyDown", "right"),
            0.1,
            ("keyUp", "right"),
            1.5,
            "up",
            ("keyDown", "right"),
        ],
        "4": [
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
        ],
        "5": [
            ("keyDown", "left"),
            1.5,
            ("keyUp", "left"),
            ("keyDown", "right"),
            1.8,
            ("keyUp", "right"),
            0.6,
            ("keyDown", "left"),
            "up",
            3,
        ],
    },
    "push": {
        "1": [
            ("keyDown", "right"),
            1.2,
            "up",
            0.4,
            ("keyUp", "right"),
            0.8,
            ("keyDown", "left"),
            "up",
            0.2,
            ("keyUp", "left"),
            ("keyDown", "right"),
            "up",
        ],
        "2": [("keyDown", "right"), 1.8, "up"],
        "3": [("keyDown", "right"), 0.1, "up", 1.5, "up"],
        "4": [
            0.5,
            ("keyDown", "right"),
            0.4,
            ("keyUp", "right"),
            ("keyDown", "left"),
            0.2,
            "up",
            0.01,
            ("keyUp", "left"),
            ("keyDown", "right"),
            0.1,
            ("keyUp", "right"),
            2.7,
            ("keyDown", "right"),
            0.5,
            "up",
        ],
        "5": [
            ("keyDown", "left"),
            2.7,
            "up",
            0.01,
            ("keyUp", "left"),
            0.3,
            ("keyDown", "right"),
            0.3,
            ("keyUp", "right"),
            ("keyDown", "left"),
            "up",
        ],
    },
    "coins": {
        "1": [("keyDown", "right"), 2, "up"],
        "2": [("keyDown", "right"), 0.3, "up", 1.3, "up"],
        "3": [
            ("keyDown", "right"),
        ],
        "4": [
            1.3,
            ("keyDown", "right"),
            0.15,
            "up",
            0.5,
            "up",
            0.1,
            "up",
            0.1,
            "up",
            0.1,
            "up",
            0.1,
            "up",
            0.1,
            "up",
            0.1,
            "up",
            0.1,
            "up",
        ],
        "5": [
            2,
            ("keyDown", "right"),
            0.2,
            "up",
            0.2,
            "up",
            0.1,
            "up",
            0.4,
            "up",
            0.2,
            "up",
            0.1,
            "up",
            0.18,
            "up",
            0.7,
            "up",
            0.2,
            "up",
            0.2,
            "up",
            0.2,
            "up",
            0.2,
            "up",
            0.2,
            "up",
            0.2,
            "up",
            0.2,
            "up",
            0.2,
            "up",
            0.2,
            "up",
            0.2,
            "up",
            0.2,
            "up",
            0.08,
            "up",
            0.08,
            "up",
            0.08,
            "up",
            0.08,
            "up",
            0.08,
            "up",
            0.08,
            "up",
            0.08,
            "up",
            0.08,
            "up",
            0.1,
            "up",
            0.3,
            ("keyUp", "right"),
        ],
    },
    "controls": {
        "1": [
            ("keyDown", "left"),
        ],
        "2": [
            ("keyUp", "right"),
            0.5,
            "up",
        ],
    },
}


def finder(folder, grayscale):
    level_screenshots = [folder+file for file in os.listdir(folder)]
    for screenshot in level_screenshots:
        try:
            location = pyautogui.locateOnScreen(
                screenshot, confidence=0.6, minSearchTime=3, grayscale=grayscale
            )
        except pyautogui.ImageNotFoundException:
            continue
        if location:
            return screenshot.split("/")[-1].split(".")[0]
    return None


loading_delay = 5

print(f"Move your focus to the window, you have {loading_delay} seconds!")
time.sleep(loading_delay)

# reset the keyss incase one is sstill being pressed
pyautogui.press("right")
pyautogui.press("left")

# Manually select a level to use
# selected_door = input("Which door are you playing? (default: pits)") or "pits"
selected_door = finder("./door_screenshots/", grayscale=False)

if selected_door is None:
    pyautogui.press("esc")
    selected_door = finder("./door_screenshots/", grayscale=False)

pyautogui.press("space")
time.sleep(2)

# selected_level = input("Which level are you playing? (default: 1)") or "1"
selected_level = finder("./level_screenshots/", grayscale=True)
selected_level = str(int(selected_level) - 1)

selected_door_index = list(levels.keys()).index(selected_door)

# loop over doors
for door in list(levels)[selected_door_index:]:
    print("\n\ndoor", door)
    time.sleep(loading_delay)
    selected_level_index = list(levels[door].keys()).index(selected_level)

    # loop over levels
    for level in list(levels[door])[selected_level_index:]:
        time.sleep(loading_delay)
        pyautogui.press("right")
        pyautogui.press("left")

        print("\nlevel", level)
        steps = levels[door][level]

        # Loop over each item in this level
        for step in steps:
            print("step", step)

            # If it's an integer or float, sleep that amount of time
            if isinstance(step, int) or isinstance(step, float):
                time.sleep(step)

            # If it's a string, press that key
            elif isinstance(step, str):
                pyautogui.press(step)

            # If it's a tuple (), then take the first value as the action (like keyDown)
            # and the second value as the key
            elif isinstance(step, tuple):
                if step[0] == "keyDown":
                    pyautogui.keyDown(step[1])
                elif step[0] == "keyUp":
                    pyautogui.keyUp(step[1])

        pyautogui.sleep(2)
        current_level = finder("./level_screenshots/", grayscale=True)
        if current_level == level:
            print("you died 💀")
            # make this retry the level