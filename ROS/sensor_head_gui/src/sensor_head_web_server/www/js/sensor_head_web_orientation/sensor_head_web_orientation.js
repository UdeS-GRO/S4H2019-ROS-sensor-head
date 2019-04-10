/*jshint esversion: 6 */

// Global variables for the orientation and velocity.
// See https://developers.google.com/web/fundamentals/native-hardware/device-orientation/
// for the images on the orientation convention.
var alpha, valpha, z;
var beta, vbeta, x;
var gamma, vgamma, y;

var alpha_offset = 0.0, beta_offset = 0.0, gamma_offset = 0.0;
var orientationMotionTimer;

var currentDevOr, lastDevOr;
var scope = {};

var lastGamma = 0,
    lastBeta = 0;
var quat = [0,0,0,1];

// const sensorAbs = new AbsoluteOrientationSensor();
const sensorAbs = new RelativeOrientationSensor();
sensorAbs.onreading = () => quat = sensorAbs.quaternion;
sensorAbs.start();

// let sensor = new Gyroscope();
// sensor.start();
// var gyro = [0,0,0];
// sensor.onreading = () => {gyro = [sensor.x, sensor.y, sensor.z];
//     // console.log([sensor.x, sensor.y, sensor.z]);
//     // console.log("Angular velocity around the X-axis " + sensor.x);
//     // console.log("Angular velocity around the Y-axis " + sensor.y);
//     // console.log("Angular velocity around the Z-axis " + sensor.z);
// };



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

// var imuTopic = new ROSLIB.Topic({
//     ros: ros,
//     name: '/mobile_imu',
//     messageType: 'goemetry_msgs/Vector3'
// });


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
    currentDevOr = eventData;
    // gamma is the left-to-right tilt in degrees, where right is positive
    // const angle_threshold = 150.0;
    // const tmp = [
    //     eventData.gamma + gamma_offset,
    //     eventData.beta + beta_offset,
    //     eventData.alpha + alpha_offset
    // ];

    // if (tmp[0] - gamma > angle_threshold) {
    //     gamma_offset += -180.0 %360;
    //     gamma = tmp[0] + -180.0;
    // } else if (tmp[0] - gamma < -angle_threshold) {
    //     gamma_offset += 180.0 %360;
    //     gamma = tmp[0] + 180.0;
    // }
    // else {
    //     gamma = tmp[0];
    // }
    // gamma = (gamma+360) % 360;



    // // beta is the front-to-back tilt in degrees, where front is positive
    // if (tmp[1] - beta > angle_threshold) {
    //     beta_offset += -180.0 %360;
    //     beta = tmp[1] + -180.0;
    // } else if (tmp[1] - beta < -angle_threshold) {
    //     beta_offset += 180.0%360;
    //     beta = tmp[1] + 180.0;
    // }
    // else {
    //     beta = tmp[1];
    // }
    // beta = (beta+360) % 360 ;


    // // alpha is the compass direction the device is facing in degrees
    // if (tmp[2] - alpha > angle_threshold) {
    //     alpha_offset += -180.0 %360;
    //     alpha = tmp[2] + -180.0;
    // } else if (tmp[2] - alpha < -angle_threshold) {
    //     alpha_offset += 180.0 %360;
    //     alpha = tmp[2] + 180.0;
    // }
    // else {
    //     alpha = tmp[2];
    // }
    // alpha = (alpha+360) %360 ;
    // console.log(eventData);
    return;
}


// setup event handler to capture the acceleration event and store the most recent data in a variable
if (window.DeviceMotionEvent) {
    window.addEventListener('devicemotion', deviceMotionHandler, true);
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

function Quat2Angle( x, y, z, w ) {

    var pitch, roll, yaw;

    var test = x * y + z * w;

    if (test > 0.499) {
        yaw = 2 * Math.atan2(x, w);
        pitch = Math.PI / 2;
        roll = 0;

        var euler1 = new THREE.Vector3( pitch, roll, yaw);
        return euler1;
    }

    if (test < -0.499) {
        yaw = -2 * Math.atan2(x, w);
        pitch = -Math.PI / 2;
        roll = 0;
        var euler2 = new THREE.Vector3( pitch, roll, yaw);
        return euler2;
    }

    var sqx = x * x;
    var sqy = y * y;
    var sqz = z * z;
    yaw = Math.atan2(2 * y * w - 2 * x * z, 1 - 2 * sqy - 2 * sqz);
    pitch = Math.asin(2 * test);
    roll = Math.atan2(2 * x * w - 2 * y * z, 1 - 2 * sqx - 2 * sqz);

    var euler = new THREE.Vector3( pitch, roll, yaw);

    return euler;
}

function onScreenOrientationChangeEvent( event ) {

    scope.screenOrientation = window.orientation || 0;

}

window.addEventListener( 'orientationchange', onScreenOrientationChangeEvent, true );

var setObjectQuaternion = function () {

    var zee = new THREE.Vector3( 0, 0, 1 );

    var euler = new THREE.Euler();

    var q0 = new THREE.Quaternion();

    var q1 = new THREE.Quaternion(  - Math.sqrt( 0.5 ), 0, 0,  Math.sqrt( 0.5 ) );

    return function ( quaternion, alpha, beta, gamma, orient ) {

        euler.set( beta, alpha, - gamma, 'YXZ' );

        quaternion.setFromEuler( euler );

        quaternion.multiply( q1 );

        quaternion.multiply( q0.setFromAxisAngle( zee, - orient ) );

    };

}();


function publishImuSnapshot() {
    // let imuData = {
    //     alpha: alpha,
    //     beta: beta,
    //     gamma: gamma,
    //     valpha: valpha,
    //     vbeta: vbeta,
    //     vgamma: vgamma,
    //     x: x,
    //     y: y,
    //     z: z
    // };

    // scope.deviceOrientation = currentDevOr;
    // let devo = currentDevOr;
    let imuData = {
        // alpha: devo.alpha,
        // beta: devo.beta,
        // gamma: devo.gamma,
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


    // const beta_radian = imuData.beta ? ((imuData.beta + 360) / 360 * 2 * Math.PI) % (2 * Math.PI) : 0;
    // const gamma_radian = imuData.gamma ? ((imuData.gamma + 360) / 360 * 2 * Math.PI) % (2 * Math.PI) : 0;
    // const alpha_radian = imuData.alpha ? ((imuData.alpha + 360) / 360 * 2 * Math.PI) % (2 * Math.PI) : 0;
    // var eurlerpose = new THREE.Euler(beta_radian, gamma_radian, alpha_radian);
    // var quaternionpose = new THREE.Quaternion();
    // quaternionpose.setFromEuler(eurlerpose);



    var imuMessage = new ROSLIB.Message({
        header: {
            frame_id: "world"
        },
        // orientation: {
        //     x: quaternionpose.x,
        //     y: quaternionpose.y,
        //     z: quaternionpose.z,
        //     w: quaternionpose.w
        // },
        orientation: {
            x: quat[0],
            y: quat[1],
            z: quat[2],
            w: quat[3]
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

    // var info = {
    //     'x': imuData.beta,
    //     'y': imuData.gamma,
    //     'z': imuData.alpha,
    //     'ob': beta_offset,
    //     'og': gamma_offset,
    //     'oa': alpha_offset
    // };

    // tmp=[];
    // tmp[0]=imuData.beta;
    // tmp[1]=imuData.gamma;//<0 ? imuData.gamma-90: imuData.gamma;
    // tmp[2]= imuData.alpha;

//     var info = [
//         imuData.beta,
//         imuData.gamma-90.0,
//         imuData.alpha,
//         beta_offset,
//         gamma_offset,
//         alpha_offset, window.orientation
// ];
//     // var info = {
//     //     'x': imuData.vbeta,
//     //     'y': imuData.vgamma,
//     //     'z': imuData.valpha
//     // };

    // var alpha = scope.deviceOrientation.alpha ? THREE.Math.degToRad(scope.deviceOrientation.alpha) : 0;
    // var beta = scope.deviceOrientation.beta ? THREE.Math.degToRad(scope.deviceOrientation.beta) : 0;
    // var gamma = scope.deviceOrientation.gamma ? THREE.Math.degToRad(scope.deviceOrientation.gamma) : 0;
    // var orient = scope.screenOrientation ? THREE.Math.degToRad(scope.screenOrientation) : 0;
     
    // var currentQ = quaternionpose; //new THREE.Quaternion().copy(scope.object.quaternion);
     
    // setObjectQuaternion(currentQ, alpha, beta, gamma, orient);
    // var currentAngle = Quat2Angle(currentQ.x, currentQ.y, currentQ.z, currentQ.w);
    // var radDeg = 180 / Math.PI;
     
    // // rotateLeft(lastGamma - currentAngle.z);
    // lastGamma = currentAngle.z;
     
    // // rotateUp(lastBeta - currentAngle.y);
    // lastBeta = currentAngle.y;

    // let info = [ lastGamma*180/Math.PI, lastBeta*180/Math.PI, currentAngle.x*180/Math.PI];
    
    // console.log(tmp);

// var imuMessage = new ROSLIB.Message({
//     x: gyro[0],
//     y: gyro[1],
//     z: gyro[2]
// });

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