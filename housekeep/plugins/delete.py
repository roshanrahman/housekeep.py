import enum
import send2trash
import os
import time
from threading import Thread
from queue import Queue

queue = Queue()


class delete(object):
    def __init__(self):
        self.name = "delete"
        self.description = "Performs delete on the files"
        self.queue = Queue()

    def perform_delete(self, files, on_file_success, on_file_failure, **kargs):
        trash = kargs.setdefault("trash", True)
        for f in files:
            try:
                if(trash):
                    send2trash.send2trash(f)
                else:
                    os.remove(f)
                queue.put((f, None))
            except Exception as e:
                print(e)
                queue.put((f, e))

    def run_action(self, files, on_file_success, on_file_failure, **kargs):
        t = Thread(target=self.perform_delete, args=(
            files, on_file_success, on_file_failure), kwargs=kargs)
        t.start()
        while True:
            try:
                f, e = queue.get(timeout=1)
                if(e is None):
                    on_file_success(f)
                else:
                    on_file_failure(f, e)
            except Exception as e:
                print(e)
                break
