import pyrosim.pyrosim as pyrosim

pyrosim.Start_SDF("boxes.sdf") # create a file to store world

for x in range(5):
    for y in range(5):
        size = 1
        z = 0
        for i in range(10):
            z = z + size/2 # add to middle of new box
            pyrosim.Send_Cube(name="Box" + str(i), pos=[x,y, z] , size=[size,size,size]) # make a cube
            z = z + size/2 # add to top of new box
            size = size * 0.9 # update box size

pyrosim.End() # close sdf file
