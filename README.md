

# 3-axes-Camera-ROS

## Introduction

3 axis head system, can be control by cell phone or USB controler. This open source project is part of the Robotics Engineering Project Course at the University of Sherbrooke.

# Linux configuration

The OS used for the test is Ubuntu 16.04.5 LTS (Xenial). It's a pretty standard installation. 

## Update

```bash
$ sudo apt-get update
$ sudo apt-get upgrade
```

## USB Port Permissions

In order to communicate with the OpenCR card via the usb, the user has to be added to the correct group. This [link](https://github.com/GoldenCheetah/GoldenCheetah/wiki/Allowing-your-linux-userid-permission-to-use-your-usb-device) shows all the details about this modification. But there's the **: Important: the computer need to be restarted to have the modifications applied **. 

```bash
[user@machine ~]$ sudo usermod -a -G dialout user
```

## Arduino IDE

voir deuxieme site



# OpenCR board configuration

To be able to control the Dynamixel motors via ROS, the OpenCR card need to be converted in a USB to Serial device that will make the bridge between the ROS server (on Linux) and the motors connected with the OpenCR card. 

After Arduino IDE is run, click File → Preferences in the top menu of the IDE. When the Preferences window appears, copy and paste following link to the Additional Boards Manager URLs textbox.

```
https://raw.githubusercontent.com/ROBOTIS-GIT/OpenCR/master/arduino/opencr_release/package_opencr_index.json
```



After, click Tools → Board → Boards Manager. Type OpenCR into the textbox to find the OpenCR by ROBOTIS package. After it finds out, click Install.After the installation, “INSTALLED” will be appeared. See if OpenCR Board is now on the list of Tools → Board. Click this to import the OpenCR Board source.



## Code upload

In order to the OpenCR card to make the bridge, this code need has to be uploaded. 

**TIP**: If you want to use OpenCR as U2D2, please upload `usb_to_dxl` firmware (`File` -> `Examples` -> `OpenCR` -> `10.Etc` -> `usb_to_dxl`) Then you can use `/dev/ttyACM0` port (The number of port may be different depending on setup).



Upgrade OpenCR: http://emanual.robotis.com/docs/en/parts/controller/opencr10/#install-on-mac (burner est pas vraiment nécessaire…)





# ROS

## ROS Installation

You can follow this [link](http://emanual.robotis.com/docs/en/software/dynamixel/dynamixel_workbench/) for the installation tutorial. Below, are the condensed steps that need to be taken. 

```bash
wget https://raw.githubusercontent.com/ROBOTIS-GIT/robotis_tools/master/install_ros_kinetic.sh && chmod 755 ./install_ros_kinetic.sh && bash ./install_ros_kinetic.sh
```

Once ROS is installed, you'll need to change of directory to catkin_ws/src. It is where all the ROS package will be instaled. 

```bash
cd catkin_ws/src
```

There are the libraries and package that you'll need to clone.

**Main packages**

```bash
git clone https://github.com/ROBOTIS-GIT/dynamixel-workbench.git
git clone https://github.com/ROBOTIS-GIT/dynamixel-workbench-msgs.git
```

**Dependant packages**

```bash
git clone https://github.com/ROBOTIS-GIT/DynamixelSDK.git
git clone https://github.com/ROBOTIS-GIT/open_manipulator_msgs.git
sudo apt-get install ros-kinetic-moveit-core ros-kinetic-moveit-ros-planning ros-kinetic-moveit-ros-planning-interface
```



Once all the git has been cloned, different ROS package will be installed to. 

## ROS Initilization

First, you'll need to source the correct ROS workspace in order to use ROS. 

```bash
source /opt/ros/kinetic/setup.bash
```

This node scans all ID with each Baudrate(9600, 57600, 115200, 1000000, 2000000, 3000000, 4000000) and shows how many dynamixels are connected. 

```bash
rosrun dynamixel_workbench_controllers find_dynamixel /dev/ttyUSB0
```

**WARNING**: This package is intended for `SINGLE` Dynamixel. Please connect only `One(1)` Dynamixel to your device.
If you connect multiple Dynamixels, manager would detect the **lowest ID** among connected Dynamixels. This package is to check Dynamixel status and access Dynamixel’s control table. Let’s take a look at the `single_manager.launch` file below.

```bash
cd ~/catkin_ws 
catkin_make
```

**Launch single_manager** 

Important: In order to connect this node with the connect USB port, you shall modify the port in the configuration file located TBD. 

```bash
roslaunch dynamixel_workbench_single_manager single_manager.launch
```

This package is to check Dynamixel status and access Dynamixel’s Control Table addresses via **GUI**. **WARNING**: Before you run this package, please launch [single_manager](http://emanual.robotis.com/docs/en/software/dynamixel/dynamixel_workbench/#single-manager) first.

```
rosrun dynamixel_workbench_single_manager_gui dynamixel_workbench_single_manager_gui
```

















