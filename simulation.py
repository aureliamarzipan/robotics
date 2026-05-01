from world import WORLD
from robot import ROBOT
import pybullet as p
import pybullet_data
import constants as c
import time

class SIMULATION:
    def __init__(self, context, solutionID):
        self.context = context
        self.solutionID = solutionID
        self.totalStepsLinksOnGround = 0
        if context == "DIRECT":
            self.physicsClient = p.connect(p.DIRECT)
        else:
            self.physicsClient = p.connect(p.GUI)
        p.setAdditionalSearchPath(pybullet_data.getDataPath()) # gets predefined objects e.g. plane.urdf
        p.configureDebugVisualizer(p.COV_ENABLE_GUI,0) # hides sidebars
        p.setGravity(c.GRAV_X, c.GRAV_Y, c.GRAV_Z)

        self.world = WORLD()
        self.robot = ROBOT(solutionID)

    def __del__(self):
        p.disconnect()

    def Run(self):
        for i in range(c.SIM_STEPS):
            p.stepSimulation()
            self.robot.Sense(i)
            self.totalStepsLinksOnGround += self.robot.stepLinksOnGround
            self.robot.Think()
            self.robot.Prepare_To_Act()
            self.robot.Act(i)

            if self.context == "GUI":
                time.sleep(c.SIM_TIME_SLEEP)

    def Get_Fitness(self, solutionID):
        with open("links" + str(solutionID) + ".txt", "w") as f:
            f.write(str(self.totalStepsLinksOnGround))
        f.close()
        self.robot.Get_Fitness(solutionID)