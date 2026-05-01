from solution import SOLUTION
from constants import NUMBER_OF_GENERATIONS, POPULATION_SIZE
import copy
import os

class PARALLEL_HILL_CLIMBER:
    def __init__(self):

        os.system("rm brain*.nndf")
        os.system("rm fitness*.txt")

        self.nextAvailableID = 0
        self.parents = {}
        for i in range(POPULATION_SIZE):
            self.parents[i] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1


    def Evolve(self):
        for currentGeneration in range(NUMBER_OF_GENERATIONS):
             self.Evolve_For_One_Generation()

    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        self.Evaluate(self.parents)
        self.Evaluate(self.children)
        #self.Print()
        self.Select()

    def Spawn(self):
        self.children = {}
        for i in self.parents.keys():
            self.children[i] = copy.deepcopy(self.parents[i])
            self.children[i].Set_Id(self.nextAvailableID)
            self.nextAvailableID += 1

    def Mutate(self):
        for child in self.children.values():
            child.Mutate()

    def Evaluate(self, solutions):
        for sol in solutions.values():
            sol.Create_Brain()
            sol.Create_Body()
            sol.Create_World()
            sol.Start_Simulation("DIRECT")

        for sol in solutions.values():
            sol.Wait_For_Simulation_To_End()

    def Select(self):
        for i in self.parents.keys():
            if self.parents[i].fitness > self.children[i].fitness:
                self.parents[i] = self.children[i]

    def Print(self):
        for i in self.parents.keys():
            print(self.parents[i].fitness, self.children[i].fitness)

    def Show_Best(self):
        best_parent_id = 0
        for i in self.parents.keys():
            if self.parents[i].fitness < self.parents[best_parent_id].fitness:
                best_parent_id = i

        self.parents[best_parent_id].Create_Brain()
        self.parents[best_parent_id].Create_Body()
        self.parents[best_parent_id].Create_World()
        self.parents[best_parent_id].Start_Simulation("GUI")