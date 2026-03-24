from world import WORLD
from robot import ROBOT
import pybullet as p
import pybullet_data
import constants as c
import generate as g
import time

class SIMULATION:
    def __init__(self, context):
        self.context = context
        if context == "DIRECT":
            self.physicsClient = p.connect(p.DIRECT)
        else:
            self.physicsClient = p.connect(p.GUI)
        p.setAdditionalSearchPath(pybullet_data.getDataPath()) # gets predefined objects e.g. plane.urdf
        p.configureDebugVisualizer(p.COV_ENABLE_GUI,0) # hides sidebars
        p.setGravity(c.GRAV_X, c.GRAV_Y, c.GRAV_Z)

        g.Create_World()
        g.Create_Robot()

        self.world = WORLD()
        self.robot = ROBOT()

    def __del__(self):
        p.disconnect()

    def Run(self):
        for i in range(c.SIM_STEPS):
            p.stepSimulation()
            self.robot.Sense(i)
            self.robot.Think()
            self.robot.Prepare_To_Act()
            self.robot.Act(i)

            if self.context == "GUI":
                time.sleep(c.SIM_TIME_SLEEP)

    def Get_Fitness(self):
        self.robot.Get_Fitness()