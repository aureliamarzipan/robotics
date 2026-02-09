import numpy
import matplotlib.pyplot as plt

backLegSensorValues = numpy.load("data/backLegSensorValues.npy")
frontLegSensorValues = numpy.load("data/frontLegSensorValues.npy")

plt.plot(backLegSensorValues, linewidth=3)
plt.plot(frontLegSensorValues)
plt.xlabel("Time")
plt.ylabel("Value")

plt.show()