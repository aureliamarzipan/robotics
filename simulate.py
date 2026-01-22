import pybullet as p
import pybullet_data
import time

from generate import *

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath()) # gets predefined objects e.g. plane.urdf
p.configureDebugVisualizer(p.COV_ENABLE_GUI,0) # hides sidebars

p.setGravity(0,0,-9.8)

Create_World()
Create_Robot()

planeId = p.loadURDF("plane.urdf")
p.loadSDF("world.sdf")
robotId = p.loadURDF("body.urdf")

for i in range(100000):
    p.stepSimulation()
    print(i)
    time.sleep(.01)

p.disconnect()

