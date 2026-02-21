import numpy
import constants as c
from pyrosim import pyrosim
import pybullet as p

class MOTOR:
    def __init__(self, joint_name):
        self.jointName = joint_name
        self.amplitude = c.AMPLITUDE
        self.frequency = c.FREQUENCY
        self.offset = c.PHASE_OFFSET

        self.motor_values = numpy.linspace(0, 2 * numpy.pi, c.SIM_STEPS)
        self.motor_values = self.amplitude * numpy.sin(self.frequency * self.motor_values + self.offset)

    def Set_Value(self, i, robot_id):
        pyrosim.Set_Motor_For_Joint(
            bodyIndex = robot_id,
            jointName = self.jointName,
            controlMode = p.POSITION_CONTROL,
            targetPosition = self.motor_values[i],
            maxForce = c.MAX_FORCE
        )

    def SaveValues(self):
        numpy.save("data/" + self.jointName + "MotorTargetValues.npy", self.motor_values)