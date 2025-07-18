# Level Devil Bot

## Usage

1. Install uv
1. Run `uv sync`
1. Run `uv run python hello.py`

## todo

- failing to attach to existing browser
- WIP move from detecting door images to finding door color see utils.py

## Problems:

1. ~~After finishing the last level of a door, the "checking if completed or died" scan takes too long and is running against the map instead of the level.~~
1. ~~Even after falling back using our "assuming already on map" logic, it fails to move the mouse off of the door (which messes up the color scanner) and fails to detect the second door as the active one.~~
1. ~~Our loop is moving on to the spikes door but our door detector still thinks we're on pits, so it chooses pits but plays the timings for spikes.~~