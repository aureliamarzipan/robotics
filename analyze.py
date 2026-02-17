import numpy
import matplotlib.pyplot as plt

backLegSensorValues = numpy.load("data/backLegSensorValues.npy")
frontLegSensorValues = numpy.load("data/frontLegSensorValues.npy")
targetAngles = numpy.load("data/targetAngles.npy")

#plt.plot(backLegSensorValues, linewidth=3)
#plt.plot(frontLegSensorValues)
plt.plot(targetAngles)
plt.xlabel("Time")
plt.ylabel("Value")

plt.show()