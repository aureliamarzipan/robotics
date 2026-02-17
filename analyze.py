import numpy
import matplotlib.pyplot as plt

backLegSensorValues = numpy.load("data/backLegSensorValues.npy")
frontLegSensorValues = numpy.load("data/frontLegSensorValues.npy")
BackLegTargetAngles = numpy.load("data/BackLegTargetAngles.npy")
FrontLegTargetAngles = numpy.load("data/FrontLegTargetAngles.npy")

#plt.plot(backLegSensorValues, linewidth=3)
#plt.plot(frontLegSensorValues)
plt.plot(BackLegTargetAngles, linewidth=4)
plt.plot(FrontLegTargetAngles)
plt.xlabel("Time")
plt.ylabel("Value")

plt.show()