import pyrosim.pyrosim as pyrosim

def Create_World():
    pyrosim.Start_SDF("world.sdf") # create a file to store world
    pyrosim.Send_Cube(name="Box", pos=[0,0,0.5], size=[1,1,1]) # make a cube at the origin
    pyrosim.End() # close sdf file

def Create_Robot():
    pyrosim.Start_URDF("body.urdf")
    pyrosim.Send_Cube(name="Torso", pos=[0,0,0.5], size=[1, 1, 1])
    pyrosim.End()
