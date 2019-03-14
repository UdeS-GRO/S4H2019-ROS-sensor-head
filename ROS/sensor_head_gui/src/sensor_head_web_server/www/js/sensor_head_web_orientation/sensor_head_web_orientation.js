/*jshint esversion: 6 */

// Global variables for the orientation and velocity. 
// See https://developers.google.com/web/fundamentals/native-hardware/device-orientation/
// for the images on the orientation convention.
var alpha, valpha, z;
var beta, vbeta, x;
var gamma, vgamma, y;

var orientationMotionTimer;
// Set up a global variable for the term div:
var term = document.getElementById('term');

/**
 * @description Function to return a formatted date and time string
 * @author Edouard Choinière
 * @date 2019-03-07
 * @returns {string} The formatted date and time string
 */
function getDateTimeString() {
    const event = new Date();
    const options = {
        timeZoneName: 'short'
    };
    return event.toLocaleString(options);
}

/**
 * @description Function to log to the fake console
 * @author Edouard Choinière
 * @date 2019-03-07
 * @param {string} consoleLineString The string to log to the fake console
 */
function termLog(consoleLineString) {
    term.innerHTML += "[" + getDateTimeString() + "] " + consoleLineString + "<br/>";
    term.scrollTop = term.scrollHeight;
}



// setup connection to the ROS server and prepare the topic
var ros = new ROSLIB.Ros();

ros.on('connection', function () {
    console.log('Connected to websocket server.');
    termLog('Connected to websocket server.');
});

ros.on('error', function (error) {
    console.log('Error connecting to websocket server: ', JSON.stringify(error));
    console.log(error);
    termLog('Error connecting to websocket server: ' + JSON.stringify(error));
    window.alert('Error connecting to websocket server');
});

ros.on('close', function () {
    console.log('Connection to websocket server closed.');
    termLog('Connection to websocket server closed.');
});

var imuTopic = new ROSLIB.Topic({
    ros: ros,
    name: '/mobile_imu',
    messageType: 'sensor_msgs/Imu'
});


// Setup event handler to capture the orientation event and store the most
// recent data in a variable.
if (window.DeviceOrientationEvent) {

    // Listen for the deviceorientation event and handle the raw data
    window.addEventListener('deviceorientation', deviceOrientationHandler, false);
    termLog("Device orientation (angle) supported!");

} else {
    termLog("Device orientation (angle) not supported!");
    window.alert("Device orientation (angle) not supported!");
}

/**
 * @description Handles the DeviceOrientationEvents and assigns the current orientation angles (degrees).
 * @author Edouard Choinière
 * @date 2019-03-07
 * @param {DeviceOrientationEvent} eventData
 * @see http://wiki.ros.org/roslibjs/Tutorials/Publishing%20video%20and%20IMU%20data%20with%20roslibjs
 */
function deviceOrientationHandler(eventData) {
    // gamma is the left-to-right tilt in degrees, where right is positive
    gamma = eventData.gamma;

    // beta is the front-to-back tilt in degrees, where front is positive
    beta = eventData.beta;

    // alpha is the compass direction the device is facing in degrees
    alpha = eventData.alpha;
    // console.log(eventData);
}


// setup event handler to capture the acceleration event and store the most recent data in a variable
if (window.DeviceMotionEvent) {
    window.addEventListener('devicemotion', deviceMotionHandler, false);
    termLog("Device motion (acceleration and rotation rate) supported!");
} else {
    termLog("Device motion (acceleration and rotation rate) not supported!");
    window.alert("Device motion (acceleration and rotation rate) not supported!");
}

/**
 * @description Handles the DeviceMotionEvent and assigns the current linear acceleration (in m/s²) and rotation rate (degrees/seconds)
 * @author Edouard Choinière
 * @date 2019-03-07
 * @param {DeviceMotionEvent} eventData
 * @see http://wiki.ros.org/roslibjs/Tutorials/Publishing%20video%20and%20IMU%20data%20with%20roslibjs
 */
function deviceMotionHandler(eventData) {
    // Grab the acceleration from the results
    var acceleration = eventData.acceleration;
    x = acceleration.x;
    y = acceleration.y;
    z = acceleration.z;

    // Grab the rotation rate from the results
    var rotation = eventData.rotationRate;
    vgamma = rotation.gamma;
    vbeta = rotation.beta;
    valpha = rotation.alpha;
    // console.log(eventData);
}

function logOrientation(alpha_angle, beta_angle, gamma_angle) {
    const orientation = {
        alpha: alpha_angle ? alpha_angle.toFixed(3) : 0,
        beta: beta_angle ? beta_angle.toFixed(3) : 0,
        gamma: gamma_angle ? gamma_angle.toFixed(3) : 0
    };
    termLog(JSON.stringify(orientation));
}


function logMotion(accX, accY, accZ, v_alpha, v_beta, v_gamma) {
    const acceleration = {
        x: accX ? accX.toFixed(3) : 0,
        y: accY ? accY.toFixed(3) : 0,
        z: accZ ? accZ.toFixed(3) : 0
    };
    const rotationRate = {
        valpha: v_alpha ? v_alpha.toFixed(3) : 0,
        vbeta: v_beta ? v_beta.toFixed(3) : 0,
        vgamma: v_gamma ? v_gamma.toFixed(3) : 0
    };
    termLog(JSON.stringify(acceleration));
    termLog(JSON.stringify(rotationRate));
}

function publishImuSnapshot() {
    let imuData = {
        alpha: alpha,
        beta: beta,
        gamma: gamma,
        valpha: valpha,
        vbeta: vbeta,
        vgamma: vgamma,
        x: x,
        y: y,
        z: z
    };
    let orientation_covariance = [0, 0, 0, 0, 0, 0, 0, 0, 0];
    let angular_velocity_covariance = [0, 0, 0, 0, 0, 0, 0, 0, 0];
    let linear_acceleration_covariance = [0, 0, 0, 0, 0, 0, 0, 0, 0];



    if (!imuData.alpha || !imuData.beta || !imuData.gamma) {
        orientation_covariance[0] = -1;
    }
    if (!imuData.valpha || !imuData.vbeta || !imuData.vgamma) {
        angular_velocity_covariance[0] = -1;
    }
    if (!imuData.x || !imuData.y || !imuData.z) {
        linear_acceleration_covariance[0] = -1;
    }


    const beta_radian = imuData.beta ? ((imuData.beta + 360) / 360 * 2 * Math.PI) % (2 * Math.PI) : 0;
    const gamma_radian = imuData.gamma ? ((imuData.gamma + 360) / 360 * 2 * Math.PI) % (2 * Math.PI) : 0;
    const alpha_radian = imuData.alpha ? ((imuData.alpha + 360) / 360 * 2 * Math.PI) % (2 * Math.PI) : 0;
    var eurlerpose = new THREE.Euler(beta_radian, gamma_radian, alpha_radian);
    var quaternionpose = new THREE.Quaternion();
    quaternionpose.setFromEuler(eurlerpose);



    var imuMessage = new ROSLIB.Message({
        header: {
            frame_id: "world"
        },
        orientation: {
            x: quaternionpose.x,
            y: quaternionpose.y,
            z: quaternionpose.z,
            w: quaternionpose.w
        },
        orientation_covariance: orientation_covariance,
        angular_velocity: {
            x: imuData.vbeta ? imuData.vbeta : 0,
            y: imuData.vgamma ? imuData.vgamma : 0,
            z: imuData.valpha ? imuData.valpha : 0,
        },
        angular_velocity_covariance: angular_velocity_covariance,
        linear_acceleration: {
            x: imuData.x ? imuData.x : 0,
            y: imuData.y ? imuData.y : 0,
            z: imuData.z ? imuData.z : 0,
        },
        linear_acceleration_covariance: linear_acceleration_covariance,
    });

    imuTopic.publish(imuMessage);

}

// Need to use wss (secure websocket) instead of ws (websocket) since the 
// webpage is using https and all requests must be secured. Or else, the 
// browsers block the connection to the rosbridge server.
termLog("wss://" + window.location.hostname + ":9090");
ros.connect("wss://" + window.location.hostname + ":9090");
// Logs the orientation and motion every 500 milliseconds
orientationMotionTimer = setInterval(function () {
    logOrientation(alpha, beta, gamma);
    publishImuSnapshot();
    logMotion(x, y, z, valpha, vbeta, vgamma);
}, 500);