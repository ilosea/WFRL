#!/usr/bin/python
# -*- coding: utf8 -*-



class Rectangle:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = 40
        self.height = 0
        self.color = (0, 255, 0)

    @staticmethod
    def getRectangles(env):
        resourcePool = env.resourcePool

        rects = []
        x = 10
        y = 100
        for i in range(len(resourcePool)):
            taskNo = resourcePool[i].taskNo
            taskSize   = resourcePool[i].taskSize
            remainTime = resourcePool[i].remainTime

            if taskNo == -1: # idle
                finishRaito = 0
            else:
                finishRaito = (taskSize - remainTime) / taskSize

            x = x + 70
            mid = 500 * finishRaito

            ret1 = Rectangle()
            ret1.x = x
            ret1.y = y
            ret1.height = mid
            ret1.color = (255, 0, 0)
            rects.append(ret1)

            ret2 = Rectangle()
            ret2.x = x
            ret2.y = y + mid
            ret2.height = 500 - mid
            rects.append(ret2)
        return rects




