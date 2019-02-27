

# 3-axes-Camera-ROS

## Introduction

3 axis head system that can be controlled by a cell phone or a USB controller. This open-source project is part of the Robotics Engineering Project Course at the Université de Sherbrooke.

Useful links: 

- http://emanual.robotis.com/docs/en/software/dynamixel/dynamixel_workbench/#ros
- http://emanual.robotis.com/docs/en/parts/controller/opencr10/#install-on-linux
- https://github.com/GoldenCheetah/GoldenCheetah/wiki/Allowing-your-linux-userid-permission-to-use-your-usb-device

# 1- Linux configuration

## Update

If you start from a clean Linux install, please do the following commands. 

```bash
$ sudo apt-get update
$ sudo apt-get upgrade
```

## USB Port Permissions

In order to communicate with the OpenCR card via USB, the user has to be added to the correct group. This [link](https://github.com/GoldenCheetah/GoldenCheetah/wiki/Allowing-your-linux-userid-permission-to-use-your-usb-device) shows all the details about this modification. But don't forget this part: **Important: the computer needs to be restarted to have the modifications applied.**

```bash
[user@machine ~]$ sudo usermod -a -G dialout user
```

## Arduino IDE

See http://emanual.robotis.com/docs/en/parts/controller/opencr10/#install-on-linux for instructions to use the full and latest version of the Arduino IDE, not the one in the packages repository since it might be updated.

# 2- OpenCR board configuration

To be able to control the Dynamixel motors via ROS, the OpenCR card need to be converted in a USB to Serial device that will make the bridge between the ROS server (on Linux) and the motors connected with the OpenCR card. 

After Arduino IDE is run, click File → Preferences in the top menu of the IDE. When the Preferences window appears, copy and paste the following link to the Additional Boards Manager URLs text box.

```bash
https://raw.githubusercontent.com/ROBOTIS-GIT/OpenCR/master/arduino/opencr_release/package_opencr_index.json
```


Then, click Tools → Board → Boards Manager. Type OpenCR into the text box to find the OpenCR by ROBOTIS package. When you find it, click Install. After the installation, “INSTALLED” will appear on your screen. See if the OpenCR Board is now on the list of Tools → Board. Click this to import the OpenCR Board source.

## Code upload

In order to the OpenCR card to make the bridge, please upload `usb_to_dxl` firmware (`File` -> `Examples` -> `OpenCR` -> `10.Etc` -> `usb_to_dxl`) Then you can use `/dev/ttyACM0` port (The number of the port may be different depending on setup).

## Hardware

In order to test the motors, please connect a SINGLE motor, connect the power supply and power on the card. 

# 3- ROS Installation

You can follow this [link](http://emanual.robotis.com/docs/en/software/dynamixel/dynamixel_workbench/) for the installation tutorial. The ROS utilization corresponds to the section 5 of the tutorial. Below are the condensed steps that need to be taken. Below are the simplified steps. 

## Install ROS on PC

The following script will allow you to simplify the ROS installation procedure. Run the following command in a terminal window. 

```bash
wget https://raw.githubusercontent.com/ROBOTIS-GIT/robotis_tools/master/install_ros_kinetic.sh && chmod 755 ./install_ros_kinetic.sh && bash ./install_ros_kinetic.sh
```

**After install ROS, please reboot PC**

## Download ROS Packages

Once ROS is installed, you'll need to change the directory to catkin_ws/src. It is where all the ROS package will be installed. 

```bash
cd catkin_ws/src
```

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

Once all the git has been cloned, different ROS packages will be installed too. 

## ROS Initilization

First, you'll need to source the correct ROS workspace in order to use ROS from anywhere. Then, catkin_make to build all the ROS workspace. 

```bash
source /opt/ros/kinetic/setup.bash
cd ~/catkin_ws 
catkin_make
```



# 4- ROS Use for a single motor

## Find the Dynamixels connected to the OpenCR card. 

In order to see which Dynamixel motors are connected, this command needs to be executed. Change ''ACM0'' to the port used by the OpenCR card. 

```bash
rosrun dynamixel_workbench_controllers find_dynamixel /dev/ttyACM0
```



## Control a SINGLE motor with ROS (command line)

**WARNING**: This package is intended for `SINGLE` Dynamixel. Please connect only `One(1)` Dynamixel to your device. If you connect multiple Dynamixels, manager would detect the **lowest ID** among connected Dynamixels. This package is to check Dynamixel status and access Dynamixel’s control table. 

## Control a SINGLE motor with ROS (GUI)

Important: In order to connect this node with the connect USB port, you shall modify the port in the configuration file located in the dynamixel_workbench_controllers config file. When using the ```sensor_head_gui``` package, the dynamixel_workbench_controllers configuration file does not need to be changed here, as it is supplied by the ```sensor_head_gui.launch``` file located in  ```ROS/sensor_head_gui/launch/sensor_head_gui.launch```

```bash
roslaunch dynamixel_workbench_single_manager single_manager.launch
```

This package is to check Dynamixel status and access Dynamixel’s Control Table addresses via **GUI**. **WARNING**: Before you run this package, please launch [single_manager](http://emanual.robotis.com/docs/en/software/dynamixel/dynamixel_workbench/#single-manager) first.

```
rosrun dynamixel_workbench_single_manager_gui dynamixel_workbench_single_manager_gui
```

# 5- Using "sensor_head_gui" package

In order to use the package, please launch this launch file. 

```
roslaunch sensor_head_gui sensor_head_gui.launch
```

This file will launch several ROS nodes (dynamical_workbench_controllers, sensor_head_gui). If you can't find the package, please see https://answers.ros.org/question/190317/ros-cant-find-package/

The arguments in this file, as well as the two .yaml configuration files in the ```ROS/sensor_head_gui/config/``` folder, can be modified with other values if your setup is different.

















