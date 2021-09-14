import enum
import send2trash
import os
import time
from threading import Thread
from queue import Queue

queue = Queue()


class sample(object):
    def __init__(self):
        self.name = "sample"
        self.description = "Performs sample action on the files"

    def perform_sample(self, files, on_file_success, on_file_failure, **kargs):
        for f in files:
            try:
                print(f'Sample action on file {f}')
                queue.put((f, None))
            except Exception as e:
                print(e)
                queue.put((f, e))

    def run_action(self, files, on_file_success, on_file_failure, **kargs):
        t = Thread(target=self.perform_sample, args=(
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
