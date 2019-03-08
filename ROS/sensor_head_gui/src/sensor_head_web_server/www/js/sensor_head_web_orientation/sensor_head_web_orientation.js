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


// setup event handler to capture the orientation event and store the most recent data in a variable
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

}

function logOrientation(alpha_angle, beta_angle, gamma_angle) {
    const orientation = {
        alpha: alpha_angle.toFixed(3),
        beta: beta_angle.toFixed(3),
        gamma: gamma_angle.toFixed(3)
    };
    termLog(JSON.stringify(orientation));
}


function logMotion(accX, accY, accZ, v_alpha, v_beta, v_gamma) {
    const acceleration = {
        x: accX.toFixed(3),
        y: accY.toFixed(3),
        z: accZ.toFixed(3)
    };
    const rotationRate = {
        valpha: v_alpha.toFixed(3),
        vbeta: v_beta.toFixed(3),
        vgamma: v_gamma.toFixed(3)
    };
    termLog(JSON.stringify(acceleration));
    termLog(JSON.stringify(rotationRate));
}

// Logs the orientation and motion every 500 milliseconds
orientationMotionTimer = setInterval(function () {
    logOrientation(alpha, beta, gamma);
    logMotion(x, y, z, valpha, vbeta, vgamma)
}, 500);