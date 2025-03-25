This project is meant to act as a framework programing ROVs for Mate ROV 
All programing should only have to be done in the Robot and transmission folders

In order to auto install required python Libraries run command below in the directory
pip install -r requirements.txt

Network setup
connect an ethernet cable, then go to settings and switch it to manual ethernet setup
set ipv4 to '192.168.1.1' and subnet mask to '255.255.255.0'

Required Python Libraries:
    pynput (keyboard)
    pygame-ce (controllers, not pygame (pygame cause a wierd exception))
    tkinter (display, should come with python)
    pillow (camera with tkinter)
    opencv-python (camera)
    numpy (camera)

I stole Command base from FIRST robotics. Also the gui was based on shuffleboard frc. Yar Har