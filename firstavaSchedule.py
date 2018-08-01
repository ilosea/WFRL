#!/usr/bin/python
# -*- coding: utf8 -*-

import random

# -1 means hold
def getAction(env):
    taskToSchedule = env.getNewTasks()
    taskNo = -1
    vmNo   = -1

    if len(taskToSchedule) == 0:
        return taskNo, vmNo
    # elif len(taskToSchedule) > 0:
    #    multi = True

    taskNo = taskToSchedule[0]

    for i in range(len(env.resourcePool)):
        if env.resourcePool[i] == 0:
            vmNo = i

    return taskNo, vmNo

