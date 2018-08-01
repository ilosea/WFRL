#!/usr/bin/python
# -*- coding: utf8 -*-

from Environment import Environment
import time
import randomSchedule
import firstavaSchedule
import RLSchedule
from pg_network import PGBrain
import numpy as np
import pickle

# t1 = time.time()
# env = Environment(taskCount=50, save=True)
# env.workflow.print()

dbfile = open('env-50', 'rb')
env = pickle.load(dbfile)
dbfile.close()


learner = PGBrain()

isDone = False
obs = env.getObservation()
ob  = obs

for i in range(100):
    for j in range(10):
        while isDone != True:

            # action = randomSchedule.getAction(ob)
            # action = firstavaSchedule.getAction(env)
            action = RLSchedule.getAction(ob, learner)
            isDone, ob = env.step(action)
            obs = np.vstack([obs, ob])



# t2 = time.time()
# print(t2-t1)

print(env.currentTime)



