import pyautogui
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

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


def finder(folder, grayscale=False, min_search_time=3):
    level_screenshots = [folder + file for file in os.listdir(folder)]
    for screenshot in level_screenshots:
        try:
            location = pyautogui.locateOnScreen(
                screenshot,
                confidence=0.8,
                minSearchTime=min_search_time,
                grayscale=grayscale,
            )
        except pyautogui.ImageNotFoundException:
            continue
        if location:
            # Extract coordinates from location tuple
            left, top, width, height = location
            
            # Take screenshot of the matched region
            match_screenshot = pyautogui.screenshot(
                region=(left, top, width, height)
            )
            
            # Save the matched region screenshot
            match_filename = f"debugging_screenshots/match_{screenshot.split('/')[-1]}"
            match_screenshot.save(match_filename)
            
            print("Screenshot found at location", location)
            print(f"Match screenshot saved as {match_filename}")
            
            return screenshot.split("/")[-1].split(".")[0]
    return None


def play_level(steps):
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


def detect_door_and_level():
    # Manually select a level to use
    print("Looking for door...")
    selected_door = finder("./door_screenshots/")
    print("Found door?", selected_door)

    if selected_door is None:
        print("No doors found, going to map.")
        pyautogui.press("esc")
        print("Looking for door again...")
        selected_door = finder("./door_screenshots/")
        print("Found door?", selected_door)

    selected_door_index = list(levels.keys()).index(selected_door)
    print("Selected door index", selected_door_index)

    pyautogui.press("space")
    time.sleep(2)
    print("Looking for level number...")

    selected_level = finder("./level_screenshots/", grayscale=True)
    selected_level = str(int(selected_level) - 1)
    print("Found level?", selected_level)

    print("Final answer:", selected_door, selected_door_index, selected_level)
    return selected_door, selected_level, selected_door_index


loading_delay = 5



# Configure Chrome options
options = Options()
# options.add_argument('--headless=new')

# Initialize headless Chrome browser
driver = webdriver.Chrome(options=options)

# Navigate to a website
driver.get('https://poki.com/en/g/level-devil')

fs_button = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "#fullscreen-button"))
)
fs_button.click()
# print(f"Move your focus to the window, you have {loading_delay} seconds!")
# time.sleep(loading_delay)

# location = pyautogui.locateOnScreen(
# "general_screenshots/1player.png", confidence=0.8, minSearchTime=10
# )
# center = pyautogui.center(location)
pyautogui.moveTo(600, 670, duration=0.5)
pyautogui.sleep(5)
pyautogui.click()
#TODO next escape is exiting full screen instead of going to map

# reset the keyss incase one is sstill being pressed
pyautogui.press("right")
pyautogui.press("left")

selected_door, selected_level, selected_door_index = detect_door_and_level()

# Currently we check if dead too fast, and on pits door 4, we
# assume death even though success, and reset to 1 due to door selector.

# TODO: These loops need to become WHILE loops, so we can dynamically
# change levels if needed rather than always going in order.
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

        while True:
            play_level(steps)

            # Check for chomps, use colored red screenshots of the chomp screen
            # keep checking for chomps for like 10 seconds or something long
            # Once chomp is detected, delay exactly 5s or so (for the level to load), then proceed

            # use finder() on a folder with chomp screenshots in color
            chomp = finder("./general_screenshots/", min_search_time=10)

            # if chomp is detected, run this:
            if chomp:
                time.sleep(loading_delay)
            else:
                print("you died 💀")
                # Reset the door and level since we may be stuck somewhere
                door, level, _ = detect_door_and_level()
                # Reset the steps to whatever level we are now on
                steps = levels[door][level]

            # if chomp is not detected but we waited over the time limit (10s),
            # then assume we died and retry

            # current_level = finder("./level_screenshots/", grayscale=True)
            # if current_level == level:
            #     print("you died 💀")
            #     # Reset the door and level since we may be stuck somewhere
            #     door, level, _ = detect_door_and_level()
            #     # Reset the steps to whatever level we are now on
            #     steps = levels[door][level]
            # else:
            #     break

            # curently we are detecting door pits when we are not on
