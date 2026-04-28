import numpy as np
import pyrosim.pyrosim as p
import os
import random
import time
import constants as c

class SOLUTION:
    def __init__(self, id):
        self.myId = id
        self.weights = np.random.rand(c.NUM_SENSOR_NEURONS, c.NUM_MOTOR_NEURONS)
        self.weights = self.weights * 2 - 1

    def Start_Simulation(self, directOrGUI):
        os.system("python3 simulate.py " + directOrGUI + " " + str(self.myId) + " 2&>1 &")

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

        for currentRow in range(c.NUM_SENSOR_NEURONS):
            for currentCol in range(c.NUM_MOTOR_NEURONS):
                p.Send_Synapse(sourceNeuronName=currentRow, targetNeuronName=currentCol + c.NUM_SENSOR_NEURONS, weight=self.weights[currentRow, currentCol])

        p.End()

    def Create_World(self):
        p.Start_SDF("world.sdf")  # create a file to store world
        p.Send_Cube(name="Box", pos=[-2, 2, 0.5], size=[1, 1, 1])  # make a cube at the origin
        p.End()  # close sdf file

    def Create_Body(self):
        p.Start_URDF("body.urdf")
        p.Send_Cube(name="Torso", pos=[0, 0, 1], size=[1, 1, 1])
        p.Send_Joint(name="Torso_FrontLeg", parent="Torso", child="FrontLeg", type="revolute",
                    position=[0, 0.5, 1], jointAxis = "1 0 0")
        p.Send_Cube(name="FrontLeg", pos=[0, 0.5, 0], size=[0.2, 1, 0.2])
        p.Send_Joint(name="Torso_BackLeg", parent="Torso", child="BackLeg", type="revolute",
                    position=[0, -0.5, 1], jointAxis = "1 0 0")
        p.Send_Cube(name="BackLeg", pos=[0, -0.5, 0], size=[0.2, 1, 0.2])

        p.End()

    def Mutate(self):
        row = random.randint(0, c.NUM_SENSOR_NEURONS - 1)
        col = random.randint(0, c.NUM_MOTOR_NEURONS - 1)
        self.weights[row][col] = random.random() * 2 - 1

    def Set_Id(self, id):
        self.myId = id
