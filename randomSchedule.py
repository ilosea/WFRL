#!/usr/bin/python
# -*- coding: utf8 -*-

import random

# -1 means hold
def getAction(ob):

    taskNo = -1
    vmNo   = -1

    if ob[-1] == -1:
        return taskNo, vmNo
    # elif len(taskToSchedule) > 0:
    #    multi = True

    taskNo = ob[-1]
    vmNo   = random.randint(-1, 8)

    return taskNo, vmNo

