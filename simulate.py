import pybullet as p
import time

physicsClient = p.connect(p.GUI)
p.configureDebugVisualizer(p.COV_ENABLE_GUI,0) # hides sidebars

p.loadSDF("box.sdf")

for i in range(1000):
    p.stepSimulation()
    print(i)
    time.sleep(.01)

p.disconnect()

