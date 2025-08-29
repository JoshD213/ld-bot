run:
	uv run hello.py

chrome:
	chromium --remote-debugging-port=9000 --user-data-dir=./ChromeProfile &