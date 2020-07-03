import os, sys, pdb, time
p = "/home/gparmar/Desktop/github_gaparmar/ImitationLearning/"
if p not in sys.path: sys.path.append(p)
from networks import LinearPolicy
import torch
from policytester import PolicyTester

# initialize the network model
p = LinearPolicy(output_ch=2).cuda()

# load the weights from file
p.load_state_dict(torch.load("/home/gparmar/Desktop/github_gaparmar/ImitationLearning/model_450.sd"))

# initialize the simulator and load the trained model
dc = PolicyTester(policy=p)

# Run the trained model on the simulator
dc.run()