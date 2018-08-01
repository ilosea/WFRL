#!/usr/bin/python
# -*- coding: utf8 -*-

import numpy as np
import random


class Workflow:

    def __init__(self, taskCount):
        self.taskCount = taskCount
        self.DAG = np.zeros((taskCount, taskCount), dtype=int)
        self.taskSize = self.generateTaskSizeRandom()
        self.randomGenerate()

    def markAsFinished(self, taskNo):
        self.DAG[taskNo, :] = 0

    def getNewTask(self):
        newTasks = []
        for i in range(self.taskCount):
            # 判断一个任务是否可以开始（是否有前驱节点）
            flag = True
            for e in self.DAG[:,i]:
                if e != 0:
                    flag = False
            if flag:
                newTasks.append(i)

        return newTasks

    def randomGenerate(self):
        for i in range(0, self.taskCount-1):
            edge = random.randint(i + 1, self.taskCount - 1)
            self.DAG[i, edge] = 1


        for i in range(1, self.taskCount-1):
            flag = True
            for e in self.DAG[:,i]:
                if e != 0:
                    flag = False
                    break

            if flag:
                edge = random.randint(0, i - 1)
                self.DAG[edge, i] = 1

        for i in range(0, self.taskCount-1):
            for j in range(i+1, self.taskCount-1):
                if random.randint(0, 10) > 99:
                    self.DAG[i,j] = 1

    def print(self):
        print(self.DAG)
        print(self.taskSize)


    def generateTaskSizeRandom(self):
        tasksize = []
        for i in range(self.taskCount):
            if random.randint(0, 10) > 6:
                tasksize.append(random.randint(10, 19))
            else:
                tasksize.append(random.randint(1, 10))
        return tasksize



