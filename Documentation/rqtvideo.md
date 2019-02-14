Connect your USB camera to your Pi
Download the rqt package with:
```bash
sudo apt-get install ros-kinetic-rqt ros-kinetic-rqt-common-plugins
```

then download the robot plugins with:
```bash
sudo apt-get install ros-kinetic-rqt-robot-plugins
```

Upgrade with 
```bash
sudo apt-get update
sudo apt-get dist-upgrade
```

rqt is then installed on your pi

Then, you will need to see your camera feed as a ROS image
To do this, you will need to download the usb_cam package with:
```bash
sudo apt-get install ros-kinetic-usb-cam
```

then start ros with:
```bash
roscore
```
in a new terminal,write:
```bash
rosrun usb_cam usb_cam_node
```
then in another terminal, write: 
```bash
rqt
```
There, you can add your video feed by going to:
Plugins->Visualization->Image View
and select your camera image in the scrolling menu
