# TODO: move this to a confige file to change while bot is running
import pyautogui
import logging

logging.basicConfig(level=logging.INFO)

levels = {
    "pits": {
        "1": [("keyDown", "right"), 2.6, "up"],
        "2": [("keyDown", "right"), 2, "up", 0.4, "up"],
        "3": [("keyDown", "right"), 1, "up"],
        "4": [
            ("keyDown", "right"),
            "up",
        ],
        "5": [("keyDown", "right"), 2.8, "up"],
    },
    "spikes": {
        "1": [
            ("keyDown", "right"),
            0.45,
            ("keyUp", "right"),
            0.01,
            ("keyDown", "left"),
            "up",
            1.2,
            "up",
        ],
        "2": [("keyDown", "right"), 0.5, "up", 1, "up", 1.4, "up"],
        "3": [
            ("keyDown", "right"),
            0.1,
            ("keyUp", "right"),
            1.5,
            "up",
            ("keyDown", "right"),
        ],
        "4": [
            ("keyDown", "right"),
            2.3,
            "up",
            0.3,
            "up",
            0.3,
            "up",
            0.3,
            "up",
            0.3,
            "up",
        ],
        "5": [
            ("keyDown", "left"),
            1.5,
            ("keyUp", "left"),
            ("keyDown", "right"),
            1.8,
            ("keyUp", "right"),
            0.6,
            ("keyDown", "left"),
            "up",
        ],
    },
    "push": {
        "1": [
            ("keyDown", "right"),
            1.2,
            "up",
            0.4,
            ("keyUp", "right"),
            0.8,
            ("keyDown", "left"),
            "up",
            0.2,
            ("keyUp", "left"),
            ("keyDown", "right"),
            "up",
        ],
        "2": [("keyDown", "right"), 1.8, "up"],
        "3": [("keyDown", "right"), 0.1, "up", 1.5, "up"],
        "4": [
            0.5,
            ("keyDown", "right"),
            0.4,
            ("keyUp", "right"),
            ("keyDown", "left"),
            0.2,
            "up",
            0.01,
            ("keyUp", "left"),
            ("keyDown", "right"),
            0.1,
            ("keyUp", "right"),
            2.7,
            ("keyDown", "right"),
            0.5,
            "up",
        ],
        "5": [
            ("keyDown", "left"),
            2.7,
            "up",
            0.01,
            ("keyUp", "left"),
            0.3,
            ("keyDown", "right"),
            0.3,
            ("keyUp", "right"),
            ("keyDown", "left"),
            "up",
        ],
    },
    "coins": {
        "1": [("keyDown", "right"), 2, "up"],
        "2": [("keyDown", "right"), 0.3, "up", 1.3, "up"],
        "3": [
            ("keyDown", "right"),
        ],
        "4": [
            1.3,
            ("keyDown", "right"),
            0.15,
            "up",
            0.5,
            "up",
            0.1,
            "up",
            0.1,
            "up",
            0.1,
            "up",
            0.1,
            "up",
            0.1,
            "up",
            0.1,
            "up",
            0.1,
            "up",
        ],
        "5": [
            2,
            ("keyDown", "right"),
            0.5,
            "up",
            0.5,
            "up",
            0.5,
            "up",
            # ///
            1,
            "up",
            0.5,
            "up",
            0.5,
            "up",
            # ///
            1,
            "up",
            1,
            "up",
            1,
            # jump onto last step
            "up",
            ("keyUp", "right"),
            0.5,
            ("keyDown", "right"),
            "up",
            0.8,
            "up",
            0.5,
            "up",
            0.5,
            "up",
            0.5,
            "up",
            0.8,
            ("keyUp", "right"),
            ("keyDown", "left"),
        ],
    },
    "controls": {
        "1": [
            ("keyDown", "left"),
        ],
        "2": [
            ("keyDown", "right"),
            0.2,
            "up",
            1,
            "up",
            0.5,
            "up",
            0.8,
            "up",
        ],
        "3": [
            ("keyDown", "left"),
            0.7,
            "up",
            0.8,
            "up",
            0.8,
            "up",
            0.8,
            "up",
        ],
        "4": [("keyDown", "right"), 0.9, "up", 1.4, "up", 0.8, "up"],
        "5": [
            ("keyDown", "left"),
            0.8,
            "up",
            0.5,
            ("keyUp", "left"),
            0.1,
            ("keyDown", "right"),
            0.5,
            "up",
            0.3,
            ("keyUp", "right"),
            0.1,
            ("keyDown", "left"),
            0.5,
            "up",
            0.4,
            ("keyUp", "left"),
            0.1,
            ("keyDown", "right"),
            0.5,
            "up",
        ],
    },
    "platforms":{
        "1": [
            ("keyDown", "right"),
            0.5,
            ("keyUp", "right"),
            6,
            ("keyDown", "right"),
        ],
        "2": [
            3,
            ("keyDown", "left"),
            1,
            "up"
        ],
        "3": [
            ("keyDown", "right"),
            2,
            ("keyUp", "right"),
            1,
            "up",
            ("keyDown", "right"),
            ("keyUp", "right"),
            1,
            "up",
            ("keyDown", "left"),
            ("keyUp", "left"),
            1,
            "up",
            ("keyDown", "right"),
            ("keyUp", "right"),
            1,
            "up",
            ("keyDown", "left"),
            ("keyUp", "left"),
            1,
            "up",
            ("keyDown", "right"),
        ],
        "4": [
            ("keyDown", "right"),
            1,
            ("keyUp", "right"),
            1,
            "up",
            ("keyDown", "right"),
            ("keyUp", "right"),
            1,
            "up",
            ("keyDown", "right"),
            ("keyUp", "right"),
            1,
            "up",
            ("keyDown", "right"),
            ("keyUp", "right"),
            1,
            "up",
            ("keyDown", "right"),
            ("keyUp", "right"),
            5,
            1,
            "up",
            ("keyDown", "right"),
            ("keyUp", "right"),
            1,
            "up",
            ("keyDown", "right"),
            ("keyUp", "right"),
        ],
        "5": [
            ("keyDown", "right"),
            2,
            "up",
            "up",
            "up",
            "up",
            "up",
            "up",
            1,
            ("keyUp", "right"),
            1,
            ("keyDown", "right"),
            "up"
        ]
    },
    "springs":{
        "1": [
            ("keyDown", "left"),
            3,
            ("keyDown", "right"),
            3.8,
            "up",
        ],
        "2": [
            ("keyDown", "right"),
            2,
            "up",
            0.5,
            "up",
            1,
            ("keyUp", "right"),
            0.5,
            ("keyDown", "left"),
            0.2,
            ("keyDown", "right"),
        ],
        "3": [
            ("keyDown", "right"),
            1,
            ("keyUp", "right"),
            0.1,
            ("keyDown", "right"),
            0.8,
            ("keyUp", "right"),
            0.1,
             ("keyDown", "right"),
            0.8,
            ("keyUp", "right"),
            0.1,
             ("keyDown", "right"),
            0.8,
            ("keyUp", "right"),
            0.1,
             ("keyDown", "right"),
            0.8,
            ("keyUp", "right"),
            0.1,
             ("keyDown", "right"),
        ],
        "4": [
            ("keyDown", "right"),
            0.5,
            ("keyDown", "left"),
            0.3,
            ("keyDown", "right"),
        ],
        "5": [

        ],
    },
    "warps":{
        "1": [

        ],
        "2": [

        ],
        "3": [

        ],
        "4": [

        ],
        "5": [

        ],
    },
    "scale":{
        "1": [

        ],
        "2": [

        ],
        "3": [

        ],
        "4": [

        ],
        "5": [

        ],
    },
    "sdoors":{
        "1": [

        ],
        "2": [

        ],
        "3": [

        ],
        "4": [

        ],
        "5": [

        ],
    },
    "saws":{
        "1": [

        ],
        "2": [

        ],
        "3": [

        ],
        "4": [

        ],
        "5": [

        ],
    },
    "flappy":{
        "1": [

        ],
        "2": [

        ],
        "3": [

        ],
        "4": [

        ],
        "5": [

        ],
    },
     "gravity":{
        "1": [

        ],
        "2": [

        ],
        "3": [

        ],
        "4": [

        ],
        "5": [

        ],
    },
    "movement":{
        "1": [

        ],
        "2": [

        ],
        "3": [

        ],
        "4": [

        ],
        "5": [

        ],
    },
    "wraparound":{
        "1": [

        ],
        "2": [

        ],
        "3": [

        ],
        "4": [

        ],
        "5": [

        ],
    },
    "final":{
        "1": [

        ],
        "2": [

        ],
        "3": [

        ],
        "4": [

        ],
        "5": [

        ],
    },
}

# 354 564
# 562 395
# 632 533
# 460 738
# 591 877
# 561 1061
# 798 922
# 1000 613
# 1024 604
# 1061 828
# 1385 864
# 1570 955
# 1613 732
# 1655 516
# 1864 614

# NOTE: Make sure you set original_screen_width and original_screen_height
# below to whatever the screen resolution is on the screen you recorded
# these X/Y coordinates on.
original_screen_width, original_screen_height = 2560, 1440
door_positions = {
    "pits": (354, 564),
    "spikes": (562, 395),
    "push": (632, 533),
    "coins": (460, 738),
    "controls": (591, 877),
    "platforms": (561, 1061),
    "springs": (798, 922),
    "warps": (1000, 613),
    "scale": (1024, 604),
    "doors": (1061, 828),
    "saws": (1385, 864),
    "flappy": (1570, 955),
    "gravity": (1613, 732),
    "movement": (1655, 516),
    "wraparound": (1864, 614),
    "final": (2180, 749),
}

# Convert x/y positions that were specific to one screen,
# into positions specific to current computer screen resolution
def normalize_point(x, y, width=None, height=None):
    # Converts macbook-specific positions to percentage-based positions
    percent_x, percent_y = x / original_screen_width, y / original_screen_height

    # Get current-screen resolution
    if not width or not height: 
        width, height = pyautogui.size() 
        
    print("width, height:", width, height)
    print("Before x/y:", x, y)
    # Convert percentage-based positions to x/y of current screen resolution
    x, y = int(width * percent_x), int(height * percent_y)
    print("After x/y:", x, y)

    return x, y



door_positions = {
    k: normalize_point( v[0], v[1] ) for k, v in door_positions.items()
}