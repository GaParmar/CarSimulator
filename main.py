import time
import numpy as np
from threading import Thread
from controller import *
import gym
import gym_donkeycar

# initialize the donkey car gym
sim_path = "sim/DonkeySimLinux/donkey_sim.x86_64"
env_name = "donkey-mountain-track-v0"
host = "127.0.0.1"
port = 9092
env  = gym.make(env_name, exe_path=sim_path,
                host=host, port=port)
obs = env.reset()

web_controller = LocalWebController(port=8887, mode="user")
t = Thread(target=web_controller.update, args=())
t.daemon = True
# start the loop
t.start()

rate_hz = 10

while True:
    start_time = time.time()
    outputs = web_controller.run_threaded(img_arr=None)
    angle, throttle, _, _ = outputs
    angle = angle*5.0
    action = np.array([angle, throttle])
    curr_obs, reward, done, info = env.step(action)
    print(outputs, info)

    sleep_time = 1.0 / rate_hz - (time.time() - start_time)
    if sleep_time > 0.0:
        time.sleep(sleep_time)