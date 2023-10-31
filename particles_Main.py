from particles_Display import Display
from particles_Field import Field
from tkinter import mainloop
import os
import threading
from queue import Queue
import time
import time

class Parent:
    def __init__(self):
        self.main_queue = Queue()
        self.display  = Display(self)
        self.field = None
        self.pause = False
        main_queue_thread = threading.Thread(target=lambda: self. main_queue_thread())
        main_queue_thread.daemon = True
        main_queue_thread.start()
        mainloop()
    def main_queue_thread(self):
        while True: # handle objects in the queue until game_lost
            time.sleep(.25)
            try:
                next_action = self.main_queue.get(False)
                next_action()
            except Exception as e:
                if str(e) != "": print(e)
        self.main_queue.queue.clear()

if __name__ == '__main__':
    main_object = Parent()
