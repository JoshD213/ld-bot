import pyautogui
from level_timings import door_positions
import logging

logging.basicConfig(level=logging.INFO)

logging.info("move to browser")
pyautogui.sleep(5)

s = pyautogui.screenshot()

logging.info("move to cordinate")
for position in door_positions.values():
    color_found = s.getpixel(position)
    logging.info(f": color is {color_found}")

for position in door_positions.values():
    pyautogui.moveTo(position)
    pyautogui.sleep(0.5)
