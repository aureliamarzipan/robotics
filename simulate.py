import sys

from simulation import SIMULATION

simulation = SIMULATION(sys.argv[1], sys.argv[2])
simulation.Run()

simulation.Get_Fitness(sys.argv[2])