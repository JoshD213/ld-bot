import pyautogui
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import subprocess
from level_timings import levels
from utils import finder, play_level, detect_door_and_level, detect_level
import os
import json
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

SESSION_FILE = "session.json"


def save_session_info(driver):
    session_info = {"url": driver.command_executor._url, "id": driver.session_id}
    with open(SESSION_FILE, "w") as f:
        json.dump(session_info, f)


def load_session_info():
    with open(SESSION_FILE, "r") as f:
        return json.load(f)


def attach_to_session(executor_url, session_id):
    # Create a dummy driver just to hijack its session
    driver = webdriver.Remote(command_executor=executor_url, desired_capabilities={})
    driver.close()  # Close the new window
    driver.session_id = session_id
    return driver


def set_up_driver():
    driver = None
    if os.path.exists(SESSION_FILE):
        # Try to resume session
        session = load_session_info()
        try:
            driver = attach_to_session(session["url"], session["id"])
            # Test if session is still alive
            driver.title  # Will raise if session is dead
            print("Resumed existing session.")
        except WebDriverException:
            print("Session expired. Starting new browser.")
            os.remove(SESSION_FILE)
    if driver is None:
        # Start new browser
        # Configure Chrome options
        options = Options()
        # options.add_argument('--headless=new')
        # options.add_argument("user-data-dir=path/to/your/custom/profile")
        options.add_experimental_option("detach", True)
        driver = webdriver.Chrome(options=options)
        # RESUME HERE: AttributeError: 'ChromiumRemoteConnection' object has no attribute '_url'
        save_session_info(driver)
        print("Started new browser session.")
    return driver


# delete any debugging screenshots
subprocess.Popen("rm ./debugging_screenshots/*", shell=True)

loading_delay = 4

# Initialize headless Chrome browser
driver = set_up_driver()

# Navigate to a website
driver.get("https://poki.com/en/g/level-devil")

# If you want to debug issues or take screenshots, uncomment this line to
# keep the testing browser open
# time.sleep(999999)

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
pyautogui.sleep(8)
pyautogui.click()

# reset the keyss incase one is sstill being pressed
pyautogui.press("right")
pyautogui.press("left")

selected_door, selected_level, selected_door_index = detect_door_and_level()

# BUG: Currently we check if dead too fast, and on pits door 4, we
# assume death even though success, and reset to 1 due to door selector.

# TODO: These loops need to become WHILE loops, so we can dynamically
# change levels if needed rather than always going in order.
# loop over doors
for door in list(levels)[selected_door_index:]:
    print("\n\ndoor", door)
    time.sleep(loading_delay)
    pyautogui.press("space")
    selected_level_index = list(levels[door].keys()).index(selected_level)

    # loop over levels
    for level in list(levels[door])[selected_level_index:]:
        while True:
            time.sleep(loading_delay)
            pyautogui.press("right")
            pyautogui.press("left")
            print("\nlevel", level)
            steps = levels[door][level]

            # Run the steps
            play_level(steps)

            # Sleep after finishing a level, to give it time to load the next one
            # before we start scanning to see if we've gone to the next level.
            pyautogui.sleep(3)

            # TODO: Test both methods and pick one. Currently level scanner is getting incorrect
            # scan results (thought level 2 pits was level 1), and chomp scanner is not running in time
            # (chomp is over before scanning starts)

            # CHOMP METHOD: LEVEL IS WON WHEN WE SEE CHOMPS -------------------
            # Check for chomps, use colored red screenshots of the chomp screen
            # keep checking for chomps for like 10 seconds or something long
            # Once chomp is detected, delay exactly 5s or so (for the level to load), then proceed

            # # use finder() on a folder with chomp screenshots in color
            # chomp = finder("./general_screenshots/", confidence=0.5, min_search_time=10)

            # # if chomp is detected, run this:
            # if chomp:
            #     time.sleep(loading_delay)
            # else:
            #     print("you died 💀")
            #     # Reset the door and level since we may be stuck somewhere
            #     door, level, _ = detect_door_and_level()
            #     # Reset the steps to whatever level we are now on
            #     steps = levels[door][level]

            # if chomp is not detected but we waited over the time limit (10s),
            # then assume we died and retry
            # END CHOMP METHOD ------------------------------------------------

            # LEVEL SCAN METHOD -----------------------------------------------
            # Check if the level number changed, and if so, we won!
            current_level = detect_level()
            if current_level == level:
                print(current_level, level, "you died 💀")
                pyautogui.press("space")
                # Reset the door and level since we may be stuck somewhere
                # door, level, _ = detect_door_and_level()
                # Reset the steps to whatever level we are now on
                # steps = levels[door][level]
            else:
                break
            # END LEVEL SCAN METHOD -------------------------------------------

            # fix transition between doors
            # get this working before working on more advanced stuff
