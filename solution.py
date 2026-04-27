import numpy as np
import pyrosim.pyrosim as p
import os
import random
import time

class SOLUTION:
    def __init__(self, id):
        self.myId = id
        self.weights = np.random.rand(3, 2)
        self.weights = self.weights * 2 - 1
        self.Create_Brain()
        self.Create_Body()
        self.Create_World()

    def Evaluate(self, directOrGUI):
        pass


    def Start_Simulation(self, directOrGUI):
        os.system("python3 simulate.py " + directOrGUI + " " + str(self.myId) + " &")

    def Wait_For_Simulation_To_End(self):
        fitnessFileName = "fitness" + str(self.myId) + ".txt"
        while not os.path.exists(fitnessFileName):
            time.sleep(0.01)
        with open(fitnessFileName) as f:
            self.fitness = float(f.read())
        f.close()

        os.system("rm fitness" + str(self.myId) + ".txt")

    def Create_Brain(self):
        p.Start_NeuralNetwork("brain" + str(self.myId) + ".nndf")
        p.Send_Sensor_Neuron(name=0, linkName="Torso")
        p.Send_Sensor_Neuron(name=1, linkName="BackLeg")
        p.Send_Sensor_Neuron(name=2, linkName="FrontLeg")

        p.Send_Motor_Neuron(name=3, jointName="Torso_BackLeg")
        p.Send_Motor_Neuron(name=4, jointName="Torso_FrontLeg")

        for currentRow in range(3):
            for currentCol in range(1):
                p.Send_Synapse(sourceNeuronName=currentRow, targetNeuronName=currentCol + 3, weight=self.weights[currentRow, currentCol])

        p.End()

    def Create_World(self):
        p.Start_SDF("world.sdf")  # create a file to store world
        p.Send_Cube(name="Box", pos=[-2, 2, 0.5], size=[1, 1, 1])  # make a cube at the origin
        p.End()  # close sdf file

    def Create_Body(self):
        p.Start_URDF("body.urdf")
        p.Send_Cube(name="Torso", pos=[0, 0, 1.5], size=[1, 1, 1])
        p.Send_Joint(name="Torso_BackLeg", parent="Torso", child="BackLeg", type="revolute", position=[0.5, 0, 1])
        p.Send_Cube(name="BackLeg", pos=[0.5, 0, -0.5], size=[1, 1, 1])
        p.Send_Joint(name="Torso_FrontLeg", parent="Torso", child="FrontLeg", type="revolute",
                           position=[-0.5, 0, 1])
        p.Send_Cube(name="FrontLeg", pos=[-0.5, 0, -0.5], size=[1, 1, 1])

        p.End()

    def Mutate(self):
        row = random.randint(0,2)
        col = random.randint(0, 1)
        self.weights[row][col] = random.random() * 2 - 1

    def Set_Id(self, id):
        self.myId = id
