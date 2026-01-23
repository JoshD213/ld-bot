import pyautogui
from level_timings import door_positions
import logging
from colorist import ColorRGB

logging.basicConfig(level=logging.INFO)

logging.info("move to browser")
pyautogui.sleep(5)

logging.info("moving mouse out of the way before screenshotting")
pyautogui.moveTo(10, 10)

s = pyautogui.screenshot()
screenshot_size = s.size
screen_size = pyautogui.size()
retina_display = (screen_size != screenshot_size)

logging.info(f"{s.mode}, {s.size}, {s.format}")
logging.info(f"{pyautogui.size()}")

logging.info("move to cordinate")
for door, position in door_positions.items():
    x, y = position
    
    if retina_display:
        logging.info("Retina display!")
        x = x * 2
        y = y * 2

    r, g, b, a = s.getpixel((x, y))
    logging.info(f"{ColorRGB(r,g,b)}{door} {x, y}: color is this {r},{g},{b},{a}{ColorRGB(r,g,b).OFF}")


for position in door_positions.values():
    pyautogui.moveTo(position)
    pyautogui.sleep(0.5)
