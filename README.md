# Level Devil Bot

## Usage

1. Install uv, make, and chromium
1. Run `uv sync`
1. Run `make run`

## todo

- ~~since chromium does not have black bars on the sides, nor a "chrome for testing" banner on the top...move all coordinate clicks -51 pixels in both x and y~~
- ~~level detection not working need to try lowering the confidence utils.detect_level, try alternate image detection librarys https://www.perplexity.ai/search/what-better-more-modern-altare-TdlVoNGZRFyJ6B8bi.J3jQ#2~~
- ~~install add blocker in chromium to avoid end of level adds.~~
- ~~failing to attach to existing browser~~
- create dock app
- ~~WIP move from detecting door images to finding door color see utils.py~~
- ~~print out screenshot of entire screen to check for level detection errors~~

## Problems:

1. ~~browser creation works and attacthing after creation works, but attaching after disconnecting dosnt work.~~
1. ~~After finishing the last level of a door, the "checking if completed or died" scan takes too long and is running against the map instead of the level.~~
1. ~~Even after falling back using our "assuming already on map" logic, it fails to move the mouse off of the door (which messes up the color scanner) and fails to detect the second door as the active one.~~
1. ~~Our loop is moving on to the spikes door but our door detector still thinks we're on pits, so it chooses pits but plays the timings for spikes.~~\
~~ Trying to figure out why door detection and level detection are suddenly not working. Door color scanner seems to be finding weird colors, looks like maybe the x/y coordinates of our doors is off?~~

## CURRENT TASK:
scanning for levels before the we click on the door