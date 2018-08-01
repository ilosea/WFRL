#!/usr/bin/python
# -*- coding: utf8 -*-

from Environment import Environment
import time
import randomSchedule
import firstavaSchedule
import numpy as np
import pickle
import random
import math
import RLSchedule
from pg_network import PGBrain

env = Environment(taskCount=50, save=False)
# env.workflow.print()

# dbfile = open('env-50', 'rb')
# env = pickle.load(dbfile)
# dbfile.close()




def getObc(ob):
    obc = []
    for i in range(0, 3):
        obc.append(math.ceil(ob[i] / env.totalSize * 1000))
    for i in range(3, 6):
        obc.append(math.ceil(ob[i] / env.totalSize / 2 * 1000))
    for i in range(6, 9):
        obc.append(math.ceil(ob[i] / env.totalSize / 3 * 1000))
    obc.append(math.ceil(ob[9] / env.totalSize * 1000))
    obc.append(math.ceil(env.getFinishRate() * 1000))
    return obc

learner = PGBrain()

for k in range(100):
    isDone = False
    ob  = env.getObservation()
    obc = getObc(ob)
    obcs = []
    rewards = []
    actions = []

    while isDone != True:

        # 没有任务可以调度
        if ob[-1] == -1:
            env.timeProcess()
            isDone = env.isDone()
            ob = env.getObservation()
        else:
            taskNo = ob[-1]
            vmNo = RLSchedule.getAction(obc, learner)
            action.append(vmNo)

            action = [taskNo, vmNo]
            # ob[-1] = env.getFinishRate()
            # print("调度任务:", taskNo)
            isDone, ob, reward = env.step(action)
            rewards.append(reward)

            obc = getObc(ob)
            if len(obcs) == 0:
                obcs = obc
            # obs = np.vstack([obs, ob])
            obcs = np.vstack([obcs, obc])

    y_pred = learner.model(obcs)

    # Compute and print loss.
    loss = learner.loss_fn(y_pred, actions)
    # print(t, loss.item())

    learner.optimizer.zero_grad()

    loss.backward()

    loss.optimizer.step()







