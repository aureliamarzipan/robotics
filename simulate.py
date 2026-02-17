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

backLegSensorValues = numpy.zeros(1000)
frontLegSensorValues = numpy.zeros(1000)

BackLeg_amplitude = numpy.pi/4
BackLeg_frequency = 10
BackLeg_phaseOffset = 0

BackLeg_targetAngles = numpy.linspace(0, 2*numpy.pi, 1000)
BackLeg_targetAngles = BackLeg_amplitude * numpy.sin(BackLeg_frequency * BackLeg_targetAngles + BackLeg_phaseOffset)
numpy.save("data/BackLegTargetAngles.npy", BackLeg_targetAngles)

FrontLeg_amplitude = numpy.pi/4
FrontLeg_frequency = 10
FrontLeg_phaseOffset = 0
FrontLeg_targetAngles = numpy.linspace(0, 2*numpy.pi, 1000)
FrontLeg_targetAngles = FrontLeg_amplitude * numpy.sin(FrontLeg_frequency * FrontLeg_targetAngles + FrontLeg_phaseOffset)
numpy.save("data/FrontLegTargetAngles.npy", FrontLeg_targetAngles)

for i in range(1000):
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
        maxForce = 50
    )

    pyrosim.Set_Motor_For_Joint(
        bodyIndex = robotId,
        jointName = b"Torso_FrontLeg",
        controlMode = p.POSITION_CONTROL,
        targetPosition = BackLeg_targetAngles[i],
        maxForce = 50
    )

    time.sleep(.01)

numpy.save("data/backLegSensorValues.npy",backLegSensorValues)
numpy.save("data/frontLegSensorValues.npy",frontLegSensorValues)

p.disconnect()

