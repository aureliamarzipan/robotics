import sys

from simulation import SIMULATION

simulation = SIMULATION(sys.argv[1])
simulation.Run()

simulation.Get_Fitness()