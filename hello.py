import pyautogui
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
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
    """Save the session information to a JSON file"""
    session_info = {
        "session_id": driver.session_id,
        "executor_url": driver.command_executor._url,
    }

    with open(SESSION_FILE, "w") as f:
        json.dump(session_info, f)
    print(f"Session information saved: {driver.session_id}")
    return session_info


def load_session_info():
    """Load session information from a JSON file if it exists"""
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, "r") as f:
            return json.load(f)
    return None


def attach_to_existing_session(session_id, executor_url):
    """Attach to an existing browser session"""
    from selenium.webdriver.remote.webdriver import WebDriver

    # Store the original execute method
    original_execute = WebDriver.execute

    # Define a new execute method that will intercept the newSession command
    def new_command_execute(self, command, params=None):
        if command == "newSession":
            # Mock the response for newSession command
            return {"success": 0, "value": {"sessionId": session_id}}
        else:
            return original_execute(self, command, params)

    # Replace the execute method with our custom version
    WebDriver.execute = new_command_execute

    # Create a driver that will attach to the existing session
    driver = webdriver.Remote(
        command_executor=executor_url, options=webdriver.ChromeOptions()
    )

    # Set the session ID to the existing session
    driver.session_id = session_id

    # Restore the original execute method
    WebDriver.execute = original_execute

    return driver


def create_new_driver():
    """Create a new Chrome driver in detached mode"""
    options = Options()
    options.add_experimental_option(
        "detach", True
    )  # Keep browser open after script ends
    driver_service = Service(port=1234)
    driver = webdriver.Chrome(service=driver_service, options=options)
    driver.command_executor._url = "http://127.0.0.1:1234"
    # Save the session information for later reuse
    session_info = {
        "session_id": driver.session_id,
        "executor_url": driver.command_executor._url,
    }

    with open(SESSION_FILE, "w") as f:
        json.dump(session_info, f)
    print(f"Session information saved: {driver.session_id}")

    return driver


# delete any debugging screenshots
subprocess.Popen("rm ./debugging_screenshots/*", shell=True)

loading_delay = 4

session_info = load_session_info()

if session_info and session_info.get("session_id") and session_info.get("executor_url"):
    try:
        print(
            f"Attempting to reattach to existing session: {session_info['session_id']}"
        )
        driver = attach_to_existing_session(
            session_info["session_id"], session_info["executor_url"]
        )
        print("Successfully reattached to existing browser session!")
    except Exception as e:
        print(f"Failed to reattach to session: {e}")
        print("Creating new browser session...")
        driver = create_new_driver()
else:
    print("No existing session found. Creating new browser session...")
    driver = create_new_driver()

# BUG: attatched to browser but crashed

# Navigate to a website
driver.get("https://poki.com/en/g/level-devil")

# If you want to debug issues or take screenshots, uncomment this line to
# keep the testing browser open
time.sleep(999999)

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
    pyautogui.moveTo(150, 540, duration=0.5)
    pyautogui.click()
    # pyautogui.press("space")
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
