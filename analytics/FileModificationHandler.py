import time
import os
import traceback


class FileModified():
    def __init__(self, path, callback, sid):
        self.path = path
        self.callback = callback
        self.last_modified = os.path.getmtime(path)
        self.sid = sid

    def start(self):
        try:
            while True:
                time.sleep(.5)
                modified = os.path.getmtime(self.path)
                if modified != self.last_modified:
                    self.last_modified = modified
                    if self.callback(self.sid):
                        break
        except Exception as e:
            print(f"Unexpected Error: {e}")
            traceback.format_exc()
            time.sleep(1)
            self.start()
