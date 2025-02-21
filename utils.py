import pyautogui
import time
import os
from PIL import UnidentifiedImageError
from level_timings import levels


def finder(folder, grayscale=False, min_search_time=3):
    level_screenshots = [folder + file for file in os.listdir(folder)]
    for screenshot in level_screenshots:
        try:
            location = pyautogui.locateOnScreen(
                screenshot,
                confidence=0.5,
                minSearchTime=min_search_time,
                grayscale=grayscale,
            )
            if location:
                # Extract coordinates from location tuple
                left, top, width, height = location
                
                # Take screenshot of the matched region
                match_screenshot = pyautogui.screenshot(
                    region=(left, top, width, height)
                )
                
                # Save the matched region screenshot
                match_filename = f"./debugging_screenshots/match_{screenshot.split('/')[-1]}"
                match_screenshot.save(match_filename)
                
                print("Screenshot found at location", location)
                print(f"Match screenshot saved as {match_filename}")
                
                return screenshot.split("/")[-1].split(".")[0]
        # If the image we're looking for can't be found, or,
        # if the debugging screenshot can't be saved, keep looping
        except (pyautogui.ImageNotFoundException, UnidentifiedImageError):
            continue
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
        pyautogui.moveTo(140, 175, duration=0.5)
        pyautogui.sleep(2)
        pyautogui.click()
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
