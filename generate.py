import pyrosim.pyrosim as pyrosim

pyrosim.Start_SDF("box.sdf") # create a file to store world

pyrosim.Send_Cube(name="Box", pos=[0,0,0.5] , size=[1,1,1]) # make a cube

pyrosim.End() # close sdf file
