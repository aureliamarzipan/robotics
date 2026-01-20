import pyrosim.pyrosim as pyrosim

pyrosim.Start_SDF("boxes.sdf") # create a file to store world

size = 1
pos = 0
for i in range(10):
    pos = pos + size/2 # add to middle of new box
    pyrosim.Send_Cube(name="Box" + str(i), pos=[0,0, pos] , size=[size,size,size]) # make a cube
    pos = pos + size/2 # add to top of new box
    size = size * 0.9 # update box size

pyrosim.End() # close sdf file
