import rumps

class AwesomeStatusBarApp(rumps.App):
    @rumps.clicked("Preferences")
    def prefs(self, _):
        rumps.alert("jk! no preferences available!")

    @rumps.clicked("Silly button")
    def onoff(self, sender):
        sender.state = not sender.state

    @rumps.clicked("Say hi")
    def sayhi(self, _):
        rumps.notification("Awesome title", "amazing subtitle", "hi!!1")

if __name__ == "__main__":
    AwesomeStatusBarApp("ld-bot").run()

    # https://github.com/jaredks/rumps?tab=readme-ov-file

    # send notifications for things that happen in the app
    # choice menu's
    # level tester and bot starter