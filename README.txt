This project is meant to act as a framework programing ROVs for Mate ROV 
All programing should only have to be done in the Robot and transmission folders

In order to auto install required python Libraries run command below in the directory
pip install -r requirements.txt

Network setup
connect an ethernet cable, then go to settings and switch it to manual ethernet setup
set ipv4 to '192.168.1.1' and subnet mask to '255.255.255.0'

Using PuTTY to connect to nautical comp
   connect to 192.168.1.2 
   login as: materov      
   password: 1234      

run the commands:  
    ./startup.sh

Update repo from main
    ./gitpull.sh

I stole Command base from FIRST robotics. Also the gui was based on shuffleboard frc. Yar Har

