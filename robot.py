import os

import pybullet as p
import pyrosim.pyrosim as pyrosim
from motor import MOTOR
from sensor import SENSOR
import constants as c
from pyrosim.neuralNetwork import NEURAL_NETWORK


class ROBOT:
    def __init__(self, solutionID):
        self.motors = {}
        self.sensors = {}

        self.robotId = p.loadURDF("body.urdf")
        self.nn = NEURAL_NETWORK("brain" + solutionID + ".nndf")

        os.system("rm brain" + str(solutionID) + ".nndf")

        pyrosim.Prepare_To_Simulate(self.robotId)
        self.Prepare_To_Sense()
        self.Prepare_To_Act()

    def Prepare_To_Sense(self):
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName)

    def Prepare_To_Act(self):
        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName] = MOTOR(jointName)

    def Sense(self, i):
        for sensor in self.sensors.values():
            sensor.GetValue(i)

    def Act(self, i):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName).encode("utf-8")
                desiredAngle = self.nn.Get_Value_Of(neuronName) * c.MOTOR_JOINT_RANGE
                self.motors[jointName].Set_Value(desiredAngle, self.robotId)
                jointName = jointName.decode("utf-8")

    def Think(self):
        self.nn.Update()
        # self.nn.Print()

    def Get_Fitness(self, solutionId):
        stateOfLinkZero = p.getLinkState(self.robotId,0)
        positionOfLinkZero = stateOfLinkZero[0]
        xCoordinateOfLinkZero = positionOfLinkZero[0]
        with open("tmp" + str(solutionId) + ".txt", "w") as f:
            f.write(str(xCoordinateOfLinkZero))
        f.close()
        os.system("mv tmp" + str(solutionId) + ".txt fitness" + str(solutionId) + ".txt")

