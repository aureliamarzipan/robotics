import numpy
import constants as c
from pyrosim import pyrosim

class SENSOR:
    def __init__(self, linkName):
        self.linkName = linkName
        self.values = numpy.zeros(c.SIM_STEPS)

    def GetValue(self, i):
        self.values[i] = pyrosim.Get_Touch_Sensor_Value_For_Link(self.linkName)
        if i == c.SIM_STEPS-1:
            print(self.values)

    def SaveValues(self):
        numpy.save("data/" + self.linkName + "SensorValues.npy", self.values)