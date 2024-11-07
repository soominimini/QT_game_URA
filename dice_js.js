// translateZ equals to the half width of .dice
// Calculation after resizing

const visit_check = [0, 0, 0, 0, 0, 0];

var dice = document.querySelectorAll('.dice');
var dice_width = dice[0].clientWidth;
var face1 = document.querySelectorAll('.face1');
var face2 = document.querySelectorAll('.face2');
var face3 = document.querySelectorAll('.face3');
var face4 = document.querySelectorAll('.face4');
var face5 = document.querySelectorAll('.face5');
var face6 = document.querySelectorAll('.face6');

function DiceResizing() {
    Array.prototype.forEach.call(face1, function (item) {
        item.style.transform = 'rotateY(0deg) translateZ(' + dice_width / 2 + 'px)';
    });
    Array.prototype.forEach.call(face2, function (item) {
        item.style.transform = 'rotateY(90deg) translateZ(' + dice_width / 2 + 'px)';
    });
    Array.prototype.forEach.call(face3, function (item) {
        item.style.transform = 'rotateX(90deg) translateZ(' + dice_width / 2 + 'px)';
    });
    Array.prototype.forEach.call(face4, function (item) {
        item.style.transform = 'rotateX(270deg) translateZ(' + dice_width / 2 + 'px)';
    });
    Array.prototype.forEach.call(face5, function (item) {
        item.style.transform = 'rotateY(270deg) translateZ(' + dice_width / 2 + 'px)';
    });
    Array.prototype.forEach.call(face6, function (item) {
        item.style.transform = 'rotateY(180deg) translateZ(' + dice_width / 2 + 'px)';
    });
}

DiceResizing();

window.onresize = function () {
    dice_width = dice[0].clientWidth;
    DiceResizing();
};

// List of activities corresponding to dice faces
var activities = ["Hug", "Shower", "Clap", "jump", "Swim", "Run"];// Correct mapping of activities

// Randomly select a face of the dice
var RandomNumber = function () {
    var rnd = Math.floor(Math.random() * 6);  // Random number from 0 to 5
    return rnd;  // Return the index of the selected face
};

function rolling() {
    var result = RandomNumber();  // Get a random face (0 to 5)
    dice[0].classList.add('face' + (result + 1));  // Add the correct face class to the dice

    // Send the selected activity to the Flask server
    sendActivityToRobot(activities[result]);  // Use the activity associated with the rolled face
}

function sendActivityToRobot(activity) {
    fetch('http://localhost:5000/activity', {  // Flask server running on port 5000
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ activity: activity }),  // Send the selected activity
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);  // Confirm success in the browser console
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

// Rolling the dice when button is clicked
var btnRolling = document.querySelector('#btnRolling');
btnRolling.onclick = function () {
    dice[0].classList.value = "dice";  // Reset dice before rolling
    rolling();  // Call the rolling function to roll the dice
    console.log(dice[0]);
};
