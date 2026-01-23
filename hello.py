import pyautogui
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import subprocess
from level_timings import levels
from utils import (
    click_door,
    play_level,
    detect_door,
    detect_level,
    detect_if_on_map,
connect_to_webdriver
)
import logging

logging.basicConfig(level=logging.INFO)
 

def main():
    # delete any debugging screenshots
    subprocess.Popen("rm ./debugging_screenshots/*", shell=True)

    # Create or reuse a Chromium webdriver
    driver = connect_to_webdriver()
    
    # Navigate to a website
    driver.get("https://poki.com/en/g/level-devil")

    # If you want to debug issues or take screenshots, uncomment this line to
    # keep the testing browser open
    # time.sleep(999999)

    fs_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#fullscreen-button"))
    )
    fs_button.click()

    pyautogui.moveTo(578, 668, duration=0.5)
    pyautogui.sleep(10)
    pyautogui.click()

    selected_door, selected_door_index = detect_door()
    loading_delay = 4

    # loop over doors
    for door in list(levels)[selected_door_index:]:
        logging.info(f"\n\ndoor {door}")
        click_door(selected_door)
        time.sleep(loading_delay)
        
        selected_level = detect_level()
        logging.info(f"Final answer: {selected_door}, {selected_door_index}, {selected_level}")
        selected_level_index = list(levels[door].keys()).index(selected_level)

        # loop over levels
        for level in list(levels[door])[selected_level_index:]:
            while True:
                time.sleep(loading_delay)
                pyautogui.press("right")
                logging.debug("pressed right")
                pyautogui.press("left")
                logging.debug("pressed left")
                logging.info(f"\nlevel {level}")
                steps = levels[door][level]

                # Run the steps
                play_level(steps)

                # Sleep after finishing a level, to give it time to load the next one
                # before we start scanning to see if we've gone to the next level.
                pyautogui.sleep(3)

                # LEVEL SCAN METHOD -----------------------------------------------
                # Check if the level number changed, and if so, we won!
                if level == "5" and detect_if_on_map():
                    logging.info("Level 5 detected, and landed on the map")
                    break

                logging.info("checking if we completed or died ")
                current_level = detect_level()
                if current_level == level:
                    logging.info(f"{current_level}, {level}, you died 💀")
                    pyautogui.press("space")
                else:
                    break
                # END LEVEL SCAN METHOD -------------------------------------------

        # If we're on the map, we just finished a door, so go to next door
        if detect_if_on_map():
            logging.info("Going to next door")
            door_names = list(levels.keys())
            selected_door = door_names[door_names.index(door) + 1]
            selected_level = "1"
            selected_level_index = 0
        else:
            logging.info("Unsure if ready for next door, scanning")
            selected_door, _ = detect_door()
            selected_level = detect_level()


if __name__ == "__main__":
    main()
