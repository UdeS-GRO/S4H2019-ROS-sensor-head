/*jshint esversion: 6 */

// Global variables for the orientation and velocity.
// See https://developers.google.com/web/fundamentals/native-hardware/device-orientation/
// for the images on the orientation convention.
var alpha, valpha, z;
var beta, vbeta, x;
var gamma, vgamma, y;

var orientationMotionTimer;


// setup connection to the ROS server and prepare the topic
var ros = new ROSLIB.Ros();

ros.on('connection', function () {
    console.log('Connected to websocket server.');
});

ros.on('error', function (error) {
    console.log('Error connecting to websocket server: ', JSON.stringify(error));
    console.log(error);
    window.alert('Error connecting to websocket server. Are you using an unsupported iOS device? Did you try on a an Android cellphone?');
});

ros.on('close', function () {
    console.log('Connection to websocket server closed.');

});

var imuTopic = new ROSLIB.Topic({
    ros: ros,
    name: '/mobile_imu',
    messageType: 'sensor_msgs/Imu'
});

var imageTopic = new ROSLIB.Topic({
    ros: ros,
    name: '/usb_cam_node_sensor_head/image_raw/compressed',
    messageType: 'sensor_msgs/CompressedImage'
});

// Setup event handler to capture the orientation event and store the most
// recent data in a variable.
if (window.DeviceOrientationEvent) {

    // Listen for the deviceorientation event and handle the raw data
    window.addEventListener('deviceorientation', deviceOrientationHandler, false);
    console.log("Device orientation (angle) supported!");

} else {
    console.log("Device orientation (angle) not supported!");
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
    console.log("Device motion (acceleration and rotation rate) supported!");
} else {
    termLog("Device motion (acceleration and rotation rate) not supported!");
    console.log("Device motion (acceleration and rotation rate) not supported!");
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
}

function logOrientation(alpha_angle, beta_angle, gamma_angle) {
    const orientation = {
        alpha: alpha_angle ? alpha_angle.toFixed(3) : 0,
        beta: beta_angle ? beta_angle.toFixed(3) : 0,
        gamma: gamma_angle ? gamma_angle.toFixed(3) : 0
    };
    console.log(orientation);
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
    console.log(acceleration);
    console.log(rotationRate);
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


    const beta_radian =  imuData.beta ? ((imuData.beta + 360) / 360 * 2 * Math.PI) % (2 * Math.PI) : 0;
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

        // var info = {'x': imuData.beta,
        //     'y': imuData.gamma,
        //     'z':imuData.alpha };
            var info = {'x': imuData.vbeta,
            'y': imuData.vgamma,
            'z':imuData.valpha };
        console.log(valpha);
    imuTopic.publish(imuMessage);

}

// Need to use wss (secure websocket) instead of ws (websocket) since the
// webpage is using https and all requests must be secured. Or else, the
// browsers block the connection to the rosbridge server.
console.log("wss://" + window.location.hostname + ":9090");
ros.connect("wss://" + window.location.hostname + ":9090");


// Captures and publishes the orientation and motion data every x milliseconds, 
// where x is the number located after the anonymous function given for the 
// setInterval argument.
orientationMotionTimer = setInterval(function () {
    // logOrientation(alpha, beta, gamma);
    publishImuSnapshot();
    // logMotion(x, y, z, valpha, vbeta, vgamma);
}, 75);

// Subscribes to the image topic (what we call the video), and updates the src 
// attribute at each message received.
imageTopic.subscribe(function (message) {
    var imagedata = "data:image/jpeg;base64," + message.data;
    document.getElementById('camera_img').setAttribute('src', imagedata);
    // imageTopic.unsubscribe(); // Uncomment to immediately unsubscribe after the first image. 
});