import time
import numpy as np
from threading import Thread

from controller import *

web_controller = LocalWebController(port=8887, mode="user")

t = Thread(target=web_controller.update, args=())
t.daemon = True

# start the loop
t.start()

rate_hz = 10

while True:
    start_time = time.time()

    outputs = web_controller.run_threaded(img_arr=None)

    print(outputs)

    sleep_time = 1.0 / rate_hz - (time.time() - start_time)
    if sleep_time > 0.0:
        time.sleep(sleep_time)