#!/usr/bin/python
# -*- coding: utf8 -*-

from Workflow import Workflow
from VirtualMachine import VM
import numpy as np
import randomSchedule
import pickle

class Environment:

    def __init__(self, taskCount=10, save = False):
        self.taskCount = taskCount
        self.workflow  = Workflow(taskCount)
        self.workflowbak = self.workflow
        self.runningTasks  = []
        self.finishedTasks = []
        self.currentTime = 0
        self.resourcePool = []
        self.initVM()
        self.finishedSize = 0
        self.totalSize    = sum(self.workflow.taskSize)
        if save:
            dbfile = open('env-'+str(self.taskCount), 'wb')
            pickle.dump(self, dbfile)
            dbfile.close()

    def saveWorkflow(self):
        dbfile = open('env-' + str(self.taskCount), 'wb')
        pickle.dump(self, dbfile)
        dbfile.close()

    def getCurrentCost(self):
        cost = 0
        for vm in self.resourcePool:
            cost += vm.totalCost
        return cost

    def initVM(self):
        vm_large_1 = VM(speed=1.8, cost=2.3, type='large')
        vm_large_2 = VM(speed=1.8, cost=2.3, type='large')
        vm_large_3 = VM(speed=1.8, cost=2.3, type='large')

        vm_medium_1 = VM(speed=1.4, cost=1.7, type='medium')
        vm_medium_2 = VM(speed=1.4, cost=1.7, type='medium')
        vm_medium_3 = VM(speed=1.4, cost=1.7, type='medium')

        vm_small_1 = VM(speed=1, cost=1, type='small')
        vm_small_2 = VM(speed=1, cost=1, type='small')
        vm_small_3 = VM(speed=1, cost=1, type='small')

        self.resourcePool.append(vm_large_1)
        self.resourcePool.append(vm_large_2)
        self.resourcePool.append(vm_large_3)

        self.resourcePool.append(vm_medium_1)
        self.resourcePool.append(vm_medium_2)
        self.resourcePool.append(vm_medium_3)

        self.resourcePool.append(vm_small_1)
        self.resourcePool.append(vm_small_2)
        self.resourcePool.append(vm_small_3)

    def getFinishRate(self):
        return self.finishedSize / self.totalSize

    def timeProcess(self):
        self.currentTime += 0.1
        for i in range(len(self.resourcePool)):
            finishSig = self.resourcePool[i].timeProcess()
            if finishSig:
                self.setTaskFinished(self.resourcePool[i].taskNo)
                self.resourcePool[i].reset()

    def step(self, taskNo, vmNo):

        # vmNo == 1 means hold
        if vmNo != -1:
            if self.resourcePool[vmNo] <= 0:
                # print("调度任务:", taskNo, " 至VM: ", vmNo)
                self.scheduleTask(taskNo, vmNo)
            else:
                pass
                # print("=== error index")
        else:
            pass
            # print("=== hold")

        ob = self.getObservation()
        self.timeProcess()
        reward = self.getFinishRate()
        return self.isDone(), ob, reward


    def getNewTasks(self):
        pre_tasks = self.workflow.getNewTask()
        tasksToSchedule = list(set(pre_tasks) - set(self.runningTasks) - set(self.finishedTasks))
        if len(tasksToSchedule) > 0:
            tasksToSchedule.sort()
        return tasksToSchedule

    def scheduleTask(self, taskNo, vmNo):
        if self.resourcePool[vmNo].taskNo != -1:
            return 'vm_'+str(vmNo)+' currently unavailable'
        self.runningTasks.append(taskNo)
        self.resourcePool[vmNo].assignTask(taskNo, self.workflow.taskSize[taskNo])
        return 'schedule task t_'+str(taskNo)+' to vm_'+str(vmNo)

    def setTaskFinished(self, taskNo):
        self.workflow.markAsFinished(taskNo)
        self.runningTasks.remove(taskNo)
        self.finishedTasks.append(taskNo)

    def isDone(self):
        if len(self.finishedTasks) == self.workflow.taskCount:
            return True
        return False

    def reset(self):
        self.workflow = self.workflowbak
        self.runningTasks = []
        self.finishedTasks = []
        self.currentTime = 0
        self.resourcePool = []
        self.initVM()
        self.finishedSize = 0
        self.totalSize = sum(self.workflow.taskSize)



