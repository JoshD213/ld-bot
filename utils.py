import pyautogui
import time
import os
from level_timings import levels
from level_timings import door_positions
import socket
import logging
import pyscreeze
from colorist import ColorRGB
import subprocess
import json
from selenium.webdriver import Chrome, ChromeOptions

SESSION_FILE = "session.pickle"

def send_notification(message, driver):
    logging.info(message)

    try:
        driver.execute_script("""
        (function () {
            const parent = document.body;  

            if (!parent) return;

            // 2) Create the element
            const el = document.createElement('div');         
            el.className = 'ldbot-notification';                  

            // 3) Content
            el.textContent = 'MESSAGE_HERE';

            // 4) STYLES (edit this block)
            Object.assign(el.style, {
                backgroundColor: 'rgba(0, 0, 0, 0.8)',
                color: '#fff',
                padding: '1em 2em',
                position: 'fixed',
                top: '1em',
                right: '1em',
                zIndex: '99999',
                fontFamily: 'monospace',
                fontSize: '1.25rem'
            });

            // 5) Insert into DOM
            parent.appendChild(el); 

            setTimeout(function(){
                if (el) el.remove();
            }, 2000)
        })();
        """.replace( # Insert our message into the script, and make it json safe/escaped
            "MESSAGE_HERE", json.dumps(message))
        )
    except Exception:
        logging.info(f"Failed to send notification: {message}")

def connect_to_webdriver():
    logging.info("Checking for existing browser session...")
    # Check if Chrome and WebDriver service are running
    webdriver_running = is_webdriver_service_running()

    if not webdriver_running:
        logging.warning(
            f"Browser prerequisites not met - WebDriver: {webdriver_running}"
        )
        logging.warning("Creating new browser session...")

        # Launch the browser
        subprocess.Popen("chromium --remote-debugging-port=9000 --user-data-dir=./ChromeProfile &", shell=True)

    logging.info("WebDriver should be running now, attempting attachment...")

    options = ChromeOptions()
    options.add_experimental_option("debuggerAddress", "localhost:9000")
    driver = Chrome(options=options)

    # Test the connection
    driver.current_url
    send_notification("Successfully attached to browser!", driver)
    return driver


def finder(driver, folder, confidence=0.5, grayscale=False, min_search_time=3):
    level_screenshots = [folder + file for file in os.listdir(folder)]

    # Sort file list alphanumerically then REVERSE!
    # For some reason, the level detection image scanner is more accurate when checking
    # images in reverse order (54321) versus forwards where we frequently got "detected 2"
    # when on level "3" and so on.
    level_screenshots.sort()
    level_screenshots.reverse()
    send_notification(f"screenshot order: {level_screenshots}", driver)

    # Take screenshot of entire screen, to see what the bot sees
    pyautogui.screenshot().save("./debugging_screenshots/fullscreen.png")
    send_notification("Debugging fullscreen screenshot taken!", driver)

    for screenshot in level_screenshots:
        try:
            location = pyautogui.locateOnScreen(
                screenshot,
                confidence=confidence,
                minSearchTime=min_search_time,
                grayscale=grayscale,
            )
            if location:
                # Extract coordinates from location tuple
                left, top, width, height = location

                send_notification(f"debug position {left}, {top}, {width}, {height}", driver)

                # Take screenshot of the matched region
                match_screenshot = pyautogui.screenshot(
                    region=(left, top, width, height)
                )

                # NOTE: If your debug screenshot is the wrong window, you may have switched apps right before it took it.
                # Recommend you kill the app RIGHT after it takes the screenshot, using the mouse to screen corner shortcut
                # Save the matched region screenshot
                match_filename = (
                    f"./debugging_screenshots/match_{screenshot.split('/')[-1]}"
                )
                match_screenshot.save(match_filename)

                send_notification(f"Screenshot found at location {location}", driver)
                send_notification(f"Match screenshot saved as {match_filename}", driver)

                return screenshot.split("/")[-1].split(".")[0]
        # If the image we're looking for can't be found, or,
        # if the debugging screenshot can't be saved, keep looping
        except (pyautogui.ImageNotFoundException,pyscreeze.ImageNotFoundException) as err:
            logging.error(err)
            continue
    return None


def play_level(driver, steps):
    # Loop over each item in this level
    for step in steps:
        send_notification(f"step {step}", driver)

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


def detect_level(driver):
    selected_level = finder(
        driver,
        "./level_screenshots/", confidence=0.9, grayscale=True, min_search_time=2
    )
    # The screenshots are numbered by the actual level number, but our loop
    # starts at zero instead of one, so we need to -1 the number from the screenshot.
    # selected_level = str(int(selected_level) - 1)
    send_notification(f"Found level? {selected_level}", driver)

    if selected_level is None:
        selected_level = "1"
        logging.warning("couldnt find level falling back to 1")

    return selected_level



def detect_if_on_map(driver):
    """
    Returns true if the map is open, returns false if on any other screen
    """
    send_notification("Looking for pause button...", driver)
    try:
        pause_location = pyautogui.locateOnScreen(
            "general_screenshots/pause.png",
            confidence=0.7,
            minSearchTime=3,
            grayscale=True,
        )

        # If pause button is visible, we're in a level, NOT on the map
        if pause_location:
            send_notification("Pause button found! You are NOT on the map", driver)
            return False
        
    except (pyautogui.ImageNotFoundException, pyscreeze.ImageNotFoundException):
        # Errors due to not finding pause button are expected, continue and
        # return "True" (not on the map)
        pass
    
    send_notification("pause button not found, assuming you are on the map", driver)
    return True

def is_retina_display():
    """Returns true if the user's display is a retina display""" 
    s = pyautogui.screenshot()
    screenshot_size = s.size
    screen_size = pyautogui.size()
    return (screen_size != screenshot_size)

def detect_door(driver):
    # If not on the map, go to the map
    if not detect_if_on_map(driver):
        send_notification("pause button found, going to map.", driver)
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
    send_notification(f"Retina display: {retina_display}", driver)

    # yellow Color of the 'current' door, coded by RGBA
    color = (252, 247, 125)
    # Fallback door in case one isn't found
    selected_door = "pits"
    # Make sure mouse isnt hovering over a door
    # because it changes the color
    pyautogui.moveTo(100, 100, duration=0.5)

    send_notification("Scanning door colors", driver)
    for door in door_positions.keys():
        x, y = door_positions[door]

        if retina_display:
            x = x * 2
            y = y * 2

        r, g, b, a = s.getpixel((x, y))
        send_notification(f"{ColorRGB(r,g,b)}{door} color is {r},{g},{b},{a}{ColorRGB(r,g,b).OFF}", driver)

        if (r,g,b) == color:
            send_notification(f"Found door! {door}", driver)
            selected_door = door
            break

    selected_door_index = list(levels.keys()).index(selected_door)
    send_notification(f"Selected door index {selected_door_index}", driver)

    return selected_door, selected_door_index


def click_door(door_name):
    x, y = door_positions[door_name]
    
    pyautogui.click(x, y)


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
