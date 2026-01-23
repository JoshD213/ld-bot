import rumps
from hello import main 
from level_tester import level_tester
from utils import connect_to_webdriver

class AwesomeStatusBarApp(rumps.App):

    @rumps.clicked("Run Bot")
    def run_bot(self, _):
        driver = connect_to_webdriver()
        main(driver)

    @rumps.clicked("level Tester")
    def run_tester(self, _):
        driver = connect_to_webdriver()
        level_tester(driver, dock_mode=True)

if __name__ == "__main__":
    AwesomeStatusBarApp("ld-bot").run()

    # https://github.com/jaredks/rumps?tab=readme-ov-file

    # send notifications for things that happen in the app
    # choice menu's
    # level tester and bot starter