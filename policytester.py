import os, sys, pdb
import time
import numpy as np
from PIL import Image
from threading import Thread
from controller import *
import gym
import gym_donkeycar
from torchvision import transforms

class PolicyTester:
    # initialize the environment, web controller
    def __init__(self, policy):
        sim_path      = "sim/DonkeySimLinux/donkey_sim.x86_64"
        env_name      = "donkey-mountain-track-v0"
        host          = "127.0.0.1"
        port          = 9092
        self.env  = gym.make(env_name, exe_path=sim_path,
                host=host, port=port)
        self.policy = policy
    
    def reset(self):
        _ = self.env.step(np.array([0, 0]))
        _ = self.env.reset()

    def run(self, duration=60, refresh_rate=10):
        self.policy.train()
        rec_start_ts = time.time()
        obs, reward, done, info = self.env.step(np.array([0, 0]))
        while True:#time.time() < (rec_start_ts+duration):
            start_time = time.time()
            img = Image.fromarray(obs)
            img_t = transforms.ToTensor()(img).view(1,3,120,160).cuda()
            throttle, angle = self.policy(img_t)
            angle = angle.detach().view(-1).item()*5.0
            throttle = throttle.detach().view(-1).item()
            action = np.array([angle, throttle])
            print(action)
            obs, reward, done, info = self.env.step(action)

            if time.time() > (rec_start_ts+40):
                self.reset()
                rec_start_ts = time.time()

            sleep_time = 1.0 / refresh_rate - (time.time() - start_time)
            if sleep_time > 0.0:
                time.sleep(sleep_time)

