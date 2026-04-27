from solution import SOLUTION
from constants import NUMBER_OF_GENERATIONS, POPULATION_SIZE
import copy

class PARALLEL_HILL_CLIMBER:
    def __init__(self):
        self.nextAvailableID = 0
        self.parents = {}
        for i in range(POPULATION_SIZE):
            self.parents[i] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1


    def Evolve(self):
        for parent in self.parents.values():
            parent.Start_Simulation("GUI")

        for parent in self.parents.values():
            parent.Wait_For_Simulation_To_End()

        # for currentGeneration in range(NUMBER_OF_GENERATIONS):
        #      self.Evolve_For_One_Generation()

    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        self.child.Evaluate("DIRECT")
        self.Print()
        self.Select()

    def Spawn(self):
        self.child = copy.deepcopy(self.parent) # todo this should be deep copying the best parent
        self.child.SetId(self.nextAvailableID)
        self.nextAvailableID += 1

    def Mutate(self):
        self.child.Mutate()

    def Select(self):
        if (self.parent.fitness < self.child.fitness):
            self.parent = self.child

    def Print(self):
        print("\n\nparent ", self.parent.fitness, "child ", self.child.fitness, "\n")

    def Show_Best(self):
        # self.parent.Evaluate("GUI")
        pass