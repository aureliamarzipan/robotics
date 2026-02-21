import pybullet as p
import pybullet_data
import time
import numpy
import constants as c

from generate import *

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath()) # gets predefined objects e.g. plane.urdf
p.configureDebugVisualizer(p.COV_ENABLE_GUI,0) # hides sidebars

p.setGravity(c.GRAV_X,c.GRAV_Y,c.GRAV_Z)

Create_World()
Create_Robot()

planeId = p.loadURDF("plane.urdf")
p.loadSDF("world.sdf")
robotId = p.loadURDF("body.urdf")

pyrosim.Prepare_To_Simulate(robotId)

backLegSensorValues = numpy.zeros(c.SIM_STEPS)
frontLegSensorValues = numpy.zeros(c.SIM_STEPS)

BackLeg_targetAngles = numpy.linspace(0, 2*numpy.pi, c.SIM_STEPS)
BackLeg_targetAngles = c.BACKLEG_AMPLITUDE * numpy.sin(c.BACKLEG_FREQUENCY * BackLeg_targetAngles + c.BACKLEG_PHASE_OFFSET)
numpy.save("data/BackLegTargetAngles.npy", BackLeg_targetAngles)

FrontLeg_targetAngles = numpy.linspace(0, 2*numpy.pi, c.SIM_STEPS)
FrontLeg_targetAngles = c.FRONTLEG_AMPLITUDE * numpy.sin(c.FRONTLEG_FREQUENCY * FrontLeg_targetAngles + c.FRONTLEG_PHASE_OFFSET)
numpy.save("data/FrontLegTargetAngles.npy", FrontLeg_targetAngles)

for i in range(c.SIM_STEPS):
    p.stepSimulation()

    backLegTouch = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    frontLegTouch = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
    backLegSensorValues[i] = backLegTouch
    frontLegSensorValues[i] = frontLegTouch

    pyrosim.Set_Motor_For_Joint(
        bodyIndex = robotId,
        jointName = b"Torso_BackLeg",
        controlMode = p.POSITION_CONTROL,
        targetPosition = BackLeg_targetAngles[i],
        maxForce = c.BACKLEG_MAX_FORCE
    )

    pyrosim.Set_Motor_For_Joint(
        bodyIndex = robotId,
        jointName = b"Torso_FrontLeg",
        controlMode = p.POSITION_CONTROL,
        targetPosition = BackLeg_targetAngles[i],
        maxForce = c.FRONTLEG_MAX_FORCE
    )

    time.sleep(c.SIM_TIME_SLEEP)

numpy.save("data/backLegSensorValues.npy",backLegSensorValues)
numpy.save("data/frontLegSensorValues.npy",frontLegSensorValues)

p.disconnect()

