import time
import numpy as np
from threading import Thread
from controller import *
import gym
import gym_donkeycar

"""
Configuration parameters
"""
sim_path      = "sim/DonkeySimLinux/donkey_sim.x86_64"
env_name      = "donkey-mountain-track-v0"
host          = "127.0.0.1"
port          = 9092
wc_port       = 8887
wc_mode       = "user"
refresh_rate  = 20



# initialize the donkey car gym
env  = gym.make(env_name, exe_path=sim_path,
                host=host, port=port)
obs = env.reset()
# initialize the web controller
wc = LocalWebController(port=wc_port, mode=wc_mode)
wc_thread = Thread(target=wc.update, args=())
wc_thread.daemon = True
wc_thread.start()

while True:
    start_time = time.time()
    outputs = wc.run_threaded(img_arr=None)
    angle, throttle, _, _ = outputs
    angle = angle*5.0
    # throttle = 0.5
    action = np.array([angle, throttle])
    curr_obs, reward, done, info = env.step(action)
    print(action)

    sleep_time = 1.0 / refresh_rate - (time.time() - start_time)
    if sleep_time > 0.0:
        time.sleep(sleep_time)
    else:
        print("going over")