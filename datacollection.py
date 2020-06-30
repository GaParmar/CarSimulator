import os, sys, pdb
import time
import numpy as np
from PIL import Image
from threading import Thread
from controller import *
import gym
import gym_donkeycar


class DataCollector:
    # initialize the environment, web controller
    def __init__(self):
        sim_path      = "sim/DonkeySimLinux/donkey_sim.x86_64"
        env_name      = "donkey-mountain-track-v0"
        host          = "127.0.0.1"
        port          = 9092
        wc_port       = 8887
        wc_mode       = "user"
        wc = LocalWebController(port=wc_port, mode=wc_mode)
        wc_thread = Thread(target=wc.update, args=())
        wc_thread.daemon = True
        wc_thread.start()
        self.wc = wc
        self.wc_thread = wc_thread
        self.env  = gym.make(env_name, exe_path=sim_path,
                host=host, port=port)
    
    def reset(self):
        _ = self.env.step(np.array([0, 0]))
        _ = self.env.reset()

    def collect_data(self, output_folder=None, override=True, buffer_length=100, duration=60, refresh_rate=10):
        ctr = 0
        buffer = []
        if output_folder is None:
            output_folder = f"output/exp_{time.time()}"
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
        # busy wait till recording is started
        while True: 
            if self.wc.run_threaded(img_arr=None)[3] : break
        print("started recording")

        rec_start_ts = time.time()
        obs, reward, done, info = self.env.step(np.array([0, 0]))
        while time.time() < (rec_start_ts+duration):
            start_time = time.time()
            img = Image.fromarray(obs)
            angle, throttle, _, recording = self.wc.run_threaded(img_arr=img)
            action = np.array([angle*5.0, throttle])
            obs, reward, done, info = self.env.step(action)
            curr = {
                "idx"       : ctr,
                "img"       : img,
                "angle"     : angle,
                "throttle"  : throttle
            }
            ctr += 1
            buffer.append(curr)
            if len(buffer) == buffer_length:
                # save the buffer to output folder
                for e in buffer:
                    fname = os.path.join(output_folder, f"{e['idx']}_{e['angle']}_{e['throttle']}.png")
                    e["img"].save(fname)
                buffer = []
            sleep_time = 1.0 / refresh_rate - (time.time() - start_time)
            if sleep_time > 0.0:
                time.sleep(sleep_time)
        print("collection done")


if __name__ == "__main__":
    dc = DataCollector()
    dc.reset()
    dc.collect_data(duration=60)
    dc.reset()