import numpy as np
import pyrosim
import os
import random

class SOLUTION:
    def __init__(self, id):
        self.myId = id
        self.weights = np.random.rand(3, 2)
        self.weights = self.weights * 2 - 1

    def Evaluate(self, directOrGUI):
        os.system("python3 simulate.py " + directOrGUI + " &")
        with open("fitness.txt") as f:
            self.fitness = float(f.read())
        f.close()

    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")  # create a file to store world
        pyrosim.Send_Cube(name="Box", pos=[-2, 2, 0.5], size=[1, 1, 1])  # make a cube at the origin
        pyrosim.End()  # close sdf file

    def Create_Body(self):
        pyrosim.Start_URDF("body.urdf")
        pyrosim.Send_Cube(name="Torso", pos=[0, 0, 1.5], size=[1, 1, 1])
        pyrosim.Send_Joint(name="Torso_BackLeg", parent="Torso", child="BackLeg", type="revolute", position=[0.5, 0, 1])
        pyrosim.Send_Cube(name="BackLeg", pos=[0.5, 0, -0.5], size=[1, 1, 1])
        pyrosim.Send_Joint(name="Torso_FrontLeg", parent="Torso", child="FrontLeg", type="revolute",
                           position=[-0.5, 0, 1])
        pyrosim.Send_Cube(name="FrontLeg", pos=[-0.5, 0, -0.5], size=[1, 1, 1])

        pyrosim.End()

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork("brain" + self.myId + ".nndf")
        pyrosim.Send_Sensor_Neuron(name=0, linkName="Torso")
        pyrosim.Send_Sensor_Neuron(name=1, linkName="BackLeg")
        pyrosim.Send_Sensor_Neuron(name=2, linkName="FrontLeg")

        pyrosim.Send_Motor_Neuron(name=3, jointName="Torso_BackLeg")
        pyrosim.Send_Motor_Neuron(name=4, jointName="Torso_FrontLeg")

        for currentRow in range(3):
            for currentCol in range(1):
                pyrosim.Send_Synapse(sourceNeuronName=currentRow, targetNeuronName=currentCol + 3, weight=self.weights[currentRow, currentCol])

        pyrosim.End()

    def Create_Robot(self):
        self.Generate_Body()
        self.Generate_Brain()

    def Mutate(self):
        row = random.randint(0,2)
        col = random.randint(0, 1)
        self.weights[row][col] = random.random() * 2 - 1

    def Set_Id(self, id):
        self.myId = id
