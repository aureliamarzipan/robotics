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
        p.Send_Sensor_Neuron(name=0, linkName="Part0")
        p.Send_Sensor_Neuron(name=1, linkName="Part1")
        p.Send_Sensor_Neuron(name=2, linkName="Part2")
        p.Send_Sensor_Neuron(name=3, linkName="Part3")
        p.Send_Sensor_Neuron(name=4, linkName="Part4")

        p.Send_Motor_Neuron(name=5, jointName="Part0_Part1")
        p.Send_Motor_Neuron(name=6, jointName="Part1_Part2")
        p.Send_Motor_Neuron(name=7, jointName="Part2_Part3")
        p.Send_Motor_Neuron(name=8, jointName="Part3_Part4")

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
        p.Send_Cube(name="Part0", pos=[0, 0, 0.1], size=[0.5, 0.2, 0.2])

        p.Send_Joint(name="Part0_Part1", parent="Part0", child="Part1", type="revolute",
                    position=[0.25, 0, 0.1], jointAxis = "0 1 0")
        p.Send_Cube(name="Part1", pos=[0.25, 0, 0], size=[0.5, 0.2, 0.2])

        p.Send_Joint(name="Part1_Part2", parent="Part1", child="Part2", type="revolute",
                     position=[0.5, 0, 0], jointAxis="0 1 0")
        p.Send_Cube(name="Part2", pos=[0.25, 0, 0], size=[0.5, 0.2, 0.2])

        p.Send_Joint(name="Part2_Part3", parent="Part2", child="Part3", type="revolute",
                     position=[0.5, 0, 0], jointAxis="0 1 0")
        p.Send_Cube(name="Part3", pos=[0.25, 0, 0], size=[0.5, 0.2, 0.2])

        p.Send_Joint(name="Part3_Part4", parent="Part3", child="Part4", type="revolute",
                     position=[0.5, 0, 0], jointAxis="0 1 0")
        p.Send_Cube(name="Part4", pos=[0.25, 0, 0], size=[0.5, 0.2, 0.2])

        p.End()

    def Mutate(self):
        row = random.randint(0, c.NUM_SENSOR_NEURONS - 1)
        col = random.randint(0, c.NUM_MOTOR_NEURONS - 1)
        self.weights[row][col] = random.random() * 2 - 1

    def Set_Id(self, id):
        self.myId = id
