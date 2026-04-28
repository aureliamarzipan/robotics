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
        p.Send_Sensor_Neuron(name=1, linkName="FrontLeg")
        p.Send_Sensor_Neuron(name=2, linkName="BackLeg")
        p.Send_Sensor_Neuron(name=3, linkName="LeftLeg")
        p.Send_Sensor_Neuron(name=4, linkName="RightLeg")
        p.Send_Sensor_Neuron(name=5, linkName="FrontLowerLeg")
        p.Send_Sensor_Neuron(name=6, linkName="BackLowerLeg")
        p.Send_Sensor_Neuron(name=7, linkName="LeftLowerLeg")
        p.Send_Sensor_Neuron(name=8, linkName="RightLowerLeg")

        p.Send_Motor_Neuron(name=9, jointName="Torso_FrontLeg")
        p.Send_Motor_Neuron(name=10, jointName="Torso_BackLeg")
        p.Send_Motor_Neuron(name=11, jointName="Torso_LeftLeg")
        p.Send_Motor_Neuron(name=12, jointName="Torso_RightLeg")
        p.Send_Motor_Neuron(name=13, jointName="FrontLeg_FrontLowerLeg")
        p.Send_Motor_Neuron(name=14, jointName="BackLeg_BackLowerLeg")
        p.Send_Motor_Neuron(name=15, jointName="LeftLeg_LeftLowerLeg")
        p.Send_Motor_Neuron(name=16, jointName="RightLeg_RightLowerLeg")

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

        p.Send_Joint(name="FrontLeg_FrontLowerLeg", parent="FrontLeg", child="FrontLowerLeg", type="revolute",
                     position=[0, 1, 0], jointAxis="1 0 0")
        p.Send_Cube(name="FrontLowerLeg", pos=[0, 0, -0.5], size=[0.2, 0.2, 1])


        p.Send_Joint(name="Torso_BackLeg", parent="Torso", child="BackLeg", type="revolute",
                    position=[0, -0.5, 1], jointAxis = "1 0 0")
        p.Send_Cube(name="BackLeg", pos=[0, -0.5, 0], size=[0.2, 1, 0.2])

        p.Send_Joint(name="BackLeg_BackLowerLeg", parent="BackLeg", child="BackLowerLeg", type="revolute",
                     position=[0, -1, 0], jointAxis="1 0 0")
        p.Send_Cube(name="BackLowerLeg", pos=[0, 0, -0.5], size=[0.2, 0.2, 1])

        p.Send_Joint(name="Torso_LeftLeg", parent="Torso", child="LeftLeg", type="revolute",
                     position=[-0.5, 0, 1], jointAxis="0 1 0")
        p.Send_Cube(name="LeftLeg", pos=[-0.5, 0, 0], size=[1, 0.2, 0.2])

        p.Send_Joint(name="LeftLeg_LeftLowerLeg", parent="LeftLeg", child="LeftLowerLeg", type="revolute",
                      position=[-1, 0, 0], jointAxis="0 1 0")
        p.Send_Cube(name="LeftLowerLeg", pos=[0, 0, -0.5], size=[0.2, 0.2, 1])

        p.Send_Joint(name="Torso_RightLeg", parent="Torso", child="RightLeg", type="revolute",
                     position=[0.5, 0, 1], jointAxis="0 1 0")
        p.Send_Cube(name="RightLeg", pos=[0.5, 0, 0], size=[1, 0.2, 0.2])

        p.Send_Joint(name="RightLeg_RightLowerLeg", parent="RightLeg", child="RightLowerLeg", type="revolute",
                     position=[1, 0, 0], jointAxis="0 1 0")
        p.Send_Cube(name="RightLowerLeg", pos=[0, 0, -0.5], size=[0.2, 0.2, 1])

        p.End()

    def Mutate(self):
        row = random.randint(0, c.NUM_SENSOR_NEURONS - 1)
        col = random.randint(0, c.NUM_MOTOR_NEURONS - 1)
        self.weights[row][col] = random.random() * 2 - 1

    def Set_Id(self, id):
        self.myId = id
