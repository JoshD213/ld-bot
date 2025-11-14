import pyautogui
import time
import os
from level_timings import levels
from level_timings import door_positions
import socket
import logging
import pyscreeze
from colorist import ColorRGB


SESSION_FILE = "session.pickle"


def finder(folder, confidence=0.5, grayscale=False, min_search_time=3):
    level_screenshots = [folder + file for file in os.listdir(folder)]

    # Sort file list alphanumerically
    level_screenshots.sort()

    # Take screenshot of entire screen, to see what the bot sees
    pyautogui.screenshot().save("./debugging_screenshots/fullscreen.png")
    logging.info("Debugging fullscreen screenshot taken!")

    for screenshot in level_screenshots:
        try:
            location = pyscreeze.locateOnScreen(
                screenshot,
                confidence=confidence,
                minSearchTime=min_search_time,
                grayscale=grayscale,
            )
            if location:
                # Extract coordinates from location tuple
                left, top, width, height = location

                logging.info(f"debug position {left}, {top}, {width}, {height}")

                # Take screenshot of the matched region
                match_screenshot = pyautogui.screenshot(
                    region=(left, top, width, height)
                )

                # Save the matched region screenshot
                match_filename = (
                    f"./debugging_screenshots/match_{screenshot.split('/')[-1]}"
                )
                match_screenshot.save(match_filename)

                logging.info(f"Screenshot found at location {location}")
                logging.info(f"Match screenshot saved as {match_filename}")

                return screenshot.split("/")[-1].split(".")[0]
        # If the image we're looking for can't be found, or,
        # if the debugging screenshot can't be saved, keep looping
        except (pyautogui.ImageNotFoundException,pyscreeze.ImageNotFoundException) as err:
            logging.error(err)
            continue
    return None


def play_level(steps):
    # Loop over each item in this level
    for step in steps:
        logging.info(f"step {step}")

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


def detect_level():
    selected_level = finder(
        "./level_screenshots/", confidence=0.85, grayscale=True, min_search_time=1
    )
    # The screenshots are numbered by the actual level number, but our loop
    # starts at zero instead of one, so we need to -1 the number from the screenshot.
    # selected_level = str(int(selected_level) - 1)
    logging.info(f"Found level? {selected_level}")

    if selected_level is None:
        selected_level = "1"
        logging.warning("couldnt find level falling back to 1")

    return selected_level


# def detect_door_and_level():
#     door_confidence = 0.85
#     # Manually select a level to use
#     logging.info("Looking for door...")
#     selected_door = finder("./door_screenshots/", confidence=door_confidence)
#     logging.info("Found door?", selected_door)

#     if selected_door is None:
#         logging.info("No doors found, going to map.")
#         pyautogui.moveTo(140, 175, duration=0.5)
#         pyautogui.click()
#         pyautogui.sleep(0.5)
#         pyautogui.moveTo(750, 500, duration=0.5)
#         pyautogui.sleep(2)
#         pyautogui.click()
#         logging.info("Looking for door again...")
#         selected_door = finder("./door_screenshots/", confidence=door_confidence)
#         logging.info("Found door?", selected_door)

#         # if door is still not found select default door
#         if selected_door is None:
#             selected_door = "pits"

#     selected_door_index = list(levels.keys()).index(selected_door)
#     logging.info("Selected door index", selected_door_index)

#     pyautogui.press("space")
#     time.sleep(3)
#     logging.info("Looking for level number...")

#     selected_level = detect_level()

#     logging.info("Final answer:", selected_door, selected_door_index, selected_level)
#     return selected_door, selected_level, selected_door_index


def detect_if_on_map():
    # Manually select a level to use
    logging.info("Looking for pause button...")
    try:
        pause_location = pyautogui.locateOnScreen(
            "general_screenshots/pause.png",
            confidence=0.7,
            minSearchTime=3,
            grayscale=True,
        )

        if pause_location:
            return False
    except (pyautogui.ImageNotFoundException,pyscreeze.ImageNotFoundException):
        logging.info("pause button not found, assuming already on map")

    return True

def is_retina_display():
    """Returns true if the user's display is a retina display""" 
    s = pyautogui.screenshot()
    screenshot_size = s.size
    screen_size = pyautogui.size()
    return (screen_size != screenshot_size)

def detect_door_and_level():
    # If not on the map, go to the map
    if not detect_if_on_map():
        logging.info("pause button found, going to map.")
        pyautogui.moveTo(140, 175, duration=0.5)
        pyautogui.click()
        pyautogui.sleep(0.5)
        pyautogui.moveTo(750, 500, duration=0.5)
        pyautogui.sleep(2)
        pyautogui.click()

    # Let the map load
    pyautogui.sleep(2)

    s = pyautogui.screenshot()
    retina_display = is_retina_display()
    logging.info(f"Retina display: {retina_display}")

    # yellow Color of the 'current' door, coded by RGBA
    color = (252, 247, 125)
    # Fallback door in case one isn't found
    selected_door = "pits"
    # Make sure mouse isnt hovering over a door
    # because it changes the color
    pyautogui.moveTo(100, 100, duration=0.5)

    logging.info("Scanning door colors")
    for door in door_positions.keys():
        x, y = door_positions[door]

        if retina_display:
            x = x * 2
            y = y * 2

        r, g, b, a = s.getpixel((x, y))
        logging.info(f"{ColorRGB(r,g,b)}{door} color is {r},{g},{b},{a}{ColorRGB(r,g,b).OFF}")

        if (r,g,b) == color:
            logging.info(f"Found door! {door}")
            selected_door = door
            break

    selected_door_index = list(levels.keys()).index(selected_door)
    logging.info(f"Selected door index {selected_door_index}")

    pyautogui.sleep(3)

    selected_level = detect_level()
    logging.info(f"Final answer: {selected_door}, {selected_door_index}, {selected_level}")
    return selected_door, selected_level, selected_door_index


def click_door(door_name):
    x, y = door_positions[door_name]
    
    pyautogui.click(x, y)


# def find_color_on_screen():
#     color = (252, 247, 125)

#     s = pyautogui.screenshot()
#     for x in range(s.width):
#         for y in range(s.height):
#             if s.getpixel((x, y)) == color:
#                 pyautogui.click(x, y)


def is_webdriver_service_running(port=9000):
    """Check if WebDriver service is running on specified port"""

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex(("127.0.0.1", port))
    sock.close()

    if result == 0:
        logging.info(f"WebDriver service found on port {port}")
        return True
    else:
        logging.info(f"No WebDriver service found on port {port}")
        return False
