http://wiki.ros.org/joy/Tutorials/ConfiguringALinuxJoystick

Install the xbox controller driver with:
```bash
sudo apt-get install xboxdrv
```

Add controller in the USB ports of Virtualbox
Check if it is there with 
```bash
lsusb
```
then install joy with
```bash
sudo apt-get install ros-kinetic-joy
ls /dev/input/
```

Test to see which port your controller is attached to like this for example:

```bash
sudo jstest /dev/input/js2
```
Here's the mapping for our Xbox One Controller
* Axes:
	* 0: Left Joystick L/R (Analog) L = 1, R = -1
	* 1: Left Joystick U/D (Analog) U = 1, D = -1
	* 2: LT (Analog) Not pressed = 1 Max = -1
	* 3: Right Joystick L/R (Analog)
	* 4: Right Joystick U/D (Analog)
	* 5: RT (Analog)
	* 6: Cross L/R (Digital)
	* 7: Cross U/D (Digital)

* Buttons (Digital): (0 or 1)
	* 0: A
	* 1: B
	* 2: X
	* 3: Y
	* 4: L
	* 5: R
	* 6: Back
	* 7: Start
	* 8: Power
	* 9: Pressing Left Joystick
	* 10: Pressing Right Joystick

You have to make the joystick accesible to ROS with:

```bash
sudo chmod a+rw /dev/input/js2
ls -l /dev/input/js2
```

then run joy to see values of your axes and buttons that should be between -1 and 1

In different terminals, run:
```bash
roscore
```
```bash
rosparam set joy_node/dev "/dev/input/js2"
rosrun joy joy_node
``` 
and
```bash
rostopic echo joy
```

then follow the tutorial at: http://wiki.ros.org/joy/Tutorials/WritingTeleopNode
but add 
```bash
catkin_package()
```
in the CMakeLists.txt file

also do a

```bash
catkin_make
```
and source your bash
