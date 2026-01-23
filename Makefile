run:
	uv run dock.py

# The app does this automatically, this command is for manual debugging
chrome:
	chromium --remote-debugging-port=9000 --user-data-dir=./ChromeProfile &