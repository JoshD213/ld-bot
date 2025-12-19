import pyautogui
import time
from level_timings import levels
import logging
import rumps

def level_tester(doc_mode=False):
    # Manually select a level to use
    default_door = "pits"
    default_level = "1"
    if not doc_mode: 
        selected_door = input(f"Which door are you playing? ({default_door})") or default_door
        selected_level = input(f"Which level are you playing? (default: {default_level})") or default_level
    else: 
        selected_door = rumps.Window(message="which door are you playing", default_text=default_door).run()
        selected_level = rumps.Window(message="which level are you playing", default_text=default_level).run()
        # need to convert rumps response object to string
    # selected_level = int(selected_level)
    # timings = levels[door][level]
    loading_delay = 5

    logging.info(f"Move your focus to the window, you have {loading_delay} seconds!")
    time.sleep(loading_delay)

    # reset the keyss incase one is sstill being pressed
    pyautogui.press("right")
    pyautogui.press("left")

    selected_door_index = list(levels.keys()).index(selected_door)

    # loop over doors
    for door in list(levels)[selected_door_index:]:
        logging.info(f"\n\ndoor {door}")
        time.sleep(loading_delay)
        pyautogui.press("space")
        selected_level_index = list(levels[door].keys()).index(selected_level)

        # loop over levels
        for level in list(levels[door])[selected_level_index:]:
            time.sleep(loading_delay)
            pyautogui.press("right")
            pyautogui.press("left")

            logging.info(f"\nlevel {level}")
            steps = levels[door][level]

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
