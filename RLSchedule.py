#!/usr/bin/python
# -*- coding: utf8 -*-

import random
import numpy as np

# -1 means hold
def getAction(ob, learner):
    pred = learner.model(ob)
    # select action w.r.t the actions prob
    action = np.random.choice(range(len(pred)), p=pred.ravel())
    action = action - 1;
    return action

