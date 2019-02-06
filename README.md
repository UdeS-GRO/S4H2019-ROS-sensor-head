# 3-axes-Camera-ROS
3 axis head system, can be control by cell phone or USB controler.

This open source project is part of the Robotics Engineering Project Course at the University of Sherbrooke.



http://emanual.robotis.com/docs/en/software/dynamixel/dynamixel_workbench/#ros

Upgrade OpenCR: http://emanual.robotis.com/docs/en/parts/controller/opencr10/#install-on-mac (burner est pas vraiment nécessaire…)


Ajouter le user pour lire et écrire sur le port usb

https://github.com/GoldenCheetah/GoldenCheetah/wiki/Allowing-your-linux-userid-permission-to-use-your-usb-device

: sudo usermod -a -G dialout user (on met notre user à la place de user)
Redémarrer après



--Install Ubuntu Mate

Frnech Canada, French Canada Multilingual

Create Username password

--Update OpenCR (only the first time)

Install Arduino on the site

DFU-UTIL

voir deuxieme site

usb_to_dxl = file - exemples - opencrCR - etc - usb_to_dxl

Follow the tutorial on http://emanual.robotis.com/docs/en/software/dynamixel/dynamixel_workbench/

--Install ROS

sudo apt-get update

sudo apt-get upgrade

wget https://raw.githubusercontent.com/ROBOTIS-GIT/robotis_tools/master/install_ros_kinetic.sh && chmod 755 ./install_ros_kinetic.sh && bash ./install_ros_kinetic.sh¸

create catkin workspace before this step

cd catkin_ws/src

--Packages

git clone https://github.com/ROBOTIS-GIT/dynamixel-workbench.git

git clone https://github.com/ROBOTIS-GIT/dynamixel-workbench-msgs.git

git clone https://github.com/ROBOTIS-GIT/DynamixelSDK.git

git clone https://github.com/ROBOTIS-GIT/open_manipulator_msgs.git

sudo apt-get install ros-kinetic-moveit-core ros-kinetic-moveit-ros-planning ros-kinetic-moveit-ros-planning-interface

--See if motors are plugged

source /opt/ros/kinetic/setup.bash

restart computer

roscore

rosrun dynamixel_workbench_controllers find_dynamixel /dev/ttyACM0

cd ~/catkin_ws

cd ~

sudo chmod 777 /dev/ttyACM0

rosrun dynamixel_workbench_controllers find_dynamixel /dev/ttyACM0 (to see if motors are plugged)

restart computer

--Test the motors

roslaunch dynamixel_workbench_single_manager single_manager.launch

change USB0 TO ACM0 at line 5 of single_manager.launch file

sudo usermod -a -G dialout user

roslaunch dynamixel_workbench_single_manager single_manager.launch

open a new terminal

rosrun dynamixel_workbench_single_manager_gui dynamixel_workbench_single_manager_gui
