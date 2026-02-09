import pybullet as p
import pybullet_data
import time
import numpy

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

pyrosim.Prepare_To_Simulate(robotId)

backLegSensorValues = numpy.zeros(200)
frontLegSensorValues = numpy.zeros(200)

for i in range(200):
    p.stepSimulation()

    backLegTouch = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    frontLegTouch = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
    backLegSensorValues[i] = backLegTouch
    frontLegSensorValues[i] = frontLegTouch

    time.sleep(.01)

numpy.save("data/backLegSensorValues.npy",backLegSensorValues)
numpy.save("data/frontLegSensorValues.npy",frontLegSensorValues)

p.disconnect()

