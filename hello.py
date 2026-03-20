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
    send_notification
)
import logging

logging.basicConfig(level=logging.INFO)
loading_delay = 4

def main(driver):
    # delete any debugging screenshots
    subprocess.Popen("rm ./debugging_screenshots/*.png", shell=True)
    
    # Navigate to a website
    driver.get("https://poki.com/en/g/level-devil")

    # If you want to debug issues or take screenshots, uncomment this line to
    # keep the testing browser open
    # time.sleep(999999)

    send_notification("Clicking fullscreen", driver)
    fs_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#fullscreen-button"))
    )
    fs_button.click()

    send_notification("Clicking 1 Player", driver)
    time.sleep(10)
    pyautogui.moveTo(578, 668, duration=0.5)
    pyautogui.click()
    send_notification("Should be in game now", driver)

    selected_door, selected_door_index = detect_door(driver)

    # loop over doors
    for door in list(levels)[selected_door_index:]:
        send_notification(f"\n\ndoor {door}", driver)
        click_door(selected_door)
        time.sleep(loading_delay)
        
        selected_level = detect_level(driver)
        send_notification(f"Final answer: {selected_door}, {selected_door_index}, {selected_level}", driver)
        selected_level_index = list(levels[door].keys()).index(selected_level)

        # loop over levels
        for level in list(levels[door])[selected_level_index:]:
            while True:
                time.sleep(loading_delay)
                pyautogui.press("right")
                logging.debug("pressed right")
                pyautogui.press("left")
                logging.debug("pressed left")
                send_notification(f"\nlevel {level}", driver)
                steps = levels[door][level]

                # Run the steps
                play_level(driver, steps)

                # Sleep after finishing a level, to give it time to load the next one
                # before we start scanning to see if we've gone to the next level.
                pyautogui.sleep(3)

                # LEVEL SCAN METHOD -----------------------------------------------
                # Check if the level number changed, and if so, we won!
                if level == "5" and detect_if_on_map(driver):
                    send_notification("Level 5 detected, and landed on the map", driver)
                    break

                send_notification("checking if we completed or died ", driver)
                current_level = detect_level(driver)
                if current_level == level:
                    send_notification(f"{current_level}, {level}, you died 💀", driver)
                    pyautogui.press("space")
                else:
                    break
                # END LEVEL SCAN METHOD -------------------------------------------

        # If we're on the map, we just finished a door, so go to next door
        if detect_if_on_map(driver):
            send_notification("Going to next door", driver)
            door_names = list(levels.keys())
            selected_door = door_names[door_names.index(door) + 1]
            selected_level = "1"
            selected_level_index = 0
        else:
            send_notification("Unsure if ready for next door, scanning", driver)
            selected_door, _ = detect_door(driver)
            selected_level = detect_level(driver)


if __name__ == "__main__":
    from utils import connect_to_webdriver
    # Create or reuse a Chromium webdriver
    driver = connect_to_webdriver()
    main(driver)
