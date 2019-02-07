

# 3-axes-Camera-ROS

## Introduction

3 axis head system, can be control by cell phone or USB controler. This open source project is part of the Robotics Engineering Project Course at the University of Sherbrooke.







# Linux configuration

## Arduino IDE

voir deuxieme site

DFU-UTIL

## Update

```bash
$ sudo apt-get update
$ sudo apt-get upgrade
```



## USB Port Permissions

In order to communicate with the OpenCR card via the usb, the user has to be added to the correct group. This [link](https://github.com/GoldenCheetah/GoldenCheetah/wiki/Allowing-your-linux-userid-permission-to-use-your-usb-device) shows all the details about this modification. But there's the *****:

```bash
[user@machine ~]$ sudo usermod -a -G dialout user
```

**Important: the computer need to be restarted to have the modifications applied **. 





# OpenCR board configuration

http://emanual.robotis.com/docs/en/software/dynamixel/dynamixel_workbench/#ros

Upgrade OpenCR: http://emanual.robotis.com/docs/en/parts/controller/opencr10/#install-on-mac (burner est pas vraiment nécessaire…)





# ROS Installation

You can follow the: Follow the tutorial on http://emanual.robotis.com/docs/en/software/dynamixel/dynamixel_workbench/ 

wget https://raw.githubusercontent.com/ROBOTIS-GIT/robotis_tools/master/install_ros_kinetic.sh && chmod 755 ./install_ros_kinetic.sh && bash ./install_ros_kinetic.sh¸

Once ROS is installed, you'll need to change of directory to catkin_ws/src. It is where all the ROS package will be instaled. 

```bash
cd catkin_ws/src
```

There are the libraries and package that you'll need to clone.

```bash
git clone https://github.com/ROBOTIS-GIT/dynamixel-workbench.git
git clone https://github.com/ROBOTIS-GIT/dynamixel-workbench-msgs.git
git clone https://github.com/ROBOTIS-GIT/DynamixelSDK.git
git clone https://github.com/ROBOTIS-GIT/open_manipulator_msgs.git
```

Once all the git has been cloned, different ROS package will be installed to. 

```bash
sudo apt-get install ros-kinetic-moveit-core ros-kinetic-moveit-ros-planning ros-kinetic-moveit-ros-planning-interface
```



## ROS Initilization

First, you'll need to source the correct ROS workspace in order to use ROS. 

```bash
source /opt/ros/kinetic/setup.bash
```







--See if motors are plugged



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

















