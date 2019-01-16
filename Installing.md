# Installing and configuring ROS on the Raspberry Pi

Ubuntu MATE 16.04 (Xenial) and ROS Kinetic are used to ensure compatibility for when a pi-gen script will be used to create the images. Currently, pi-gen does not support Ubuntu Bionic, required for ROS Melodic. 

## Installing Ubuntu MATE 16.04

Ubuntu MATE 16.04 should be downloaded and installed on the Raspberry Pi.
<https://ubuntu-mate.org/raspberry-pi/>

## Installing ROS Kinetic

The procedure followed to install packages was from <http://wiki.ros.org/kinetic/Installation/Ubuntu>

Select the "Desktop Install" for the set of packages at step 1.4.
This might take some time (10-20 minutes or more) on the Raspberry Pi, since there is a lot of disk I/O.

See the file [installing_ros.bash](https://github.com/gene2302/3-axis-ROS-sensor-head/blob/master/installing_ros.bash) for the commands entered, or see below:
```bash
sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'

sudo apt-key adv --keyserver hkp://ha.pool.sks-keyservers.net:80 --recv-key 421C365BD9FF1F717815A3895523BAEEB01FA116

sudo apt-get update
sudo apt-get install ros-kinetic-desktop

sudo rosdep init
rosdep update

echo "source /opt/ros/kinetic/setup.bash" >> ~/.bashrc
source ~/.bashrc

sudo apt install python-rosinstall python-rosinstall-generator python-wstool build-essential

printenv | grep ROS
```
