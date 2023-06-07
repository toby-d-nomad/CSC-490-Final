var video = document.getElementById('video');
var captureBtn = document.getElementById('capture-btn');
var capturedImage = document.getElementById('captured-image');
var capturedImage = document.createElement('img');
var sendBtn = document.getElementById('submit-btn');
var capturedImageHolder = document.getElementById('capturedImageHolder');
var imageHidden = document.getElementById('staff_image')
var stream;
var imageData;

const email = document.getElementById('email');
const student_password = document.getElementById('student_password');

navigator.mediaDevices.getUserMedia({ video: true })
.then(function(stream) {
    video.srcObject = stream;
    video.play();
    stream = stream;
})
.catch(function(error) {
    console.error('Error accessing video stream:', error);
});

captureBtn.addEventListener('click', function (e) {
    e.preventDefault()
    var canvas = document.createElement('canvas');
    var context = canvas.getContext('2d');
    canvas.width = 240;
    canvas.height = 220;
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    imageData = canvas.toDataURL('image/png');
    var imageDataRes = imageData.replace("data:image/png;base64,", "")
    imageHidden.value = imageDataRes;
    // console.log(imageData);
    console.log('button-pressed');
    video.srcObject = null
    video.remove()
    video.style.display = 'none';
    capturedImage.src = imageData;
    capturedImage.style.display = 'block';
    capturedImageHolder.style.display = 'block'
    capturedImageHolder.appendChild(capturedImage)
    captureBtn.disabled = true;
})

// sendBtn.addEventListener('click', function(e) {
//     e.preventDefault()
//     let c_email = email.value
//     let c_student_password = student_password.value
//     if(c_email !== '' && c_student_password !== ''){
//         if(imageData) {
//             const upload = {
//                 'email': c_email,
//                 'password': c_student_password,
//                 'student_image': imageData
//             }
//             sendStudentAuthData(upload)
//             console.log(upload);
//         } else {
//             console.log('No Image Data Available');
//             alert('No Image Data Available')
//         }
//     } else {
//         console.log('Fill in all the required details');
//         alert('Fill in all the Required Details')
//     }
// })

// function sendStudentAuthData(upload){
//     fetch('/student', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json'
//         },
//         body: JSON.stringify(upload)
//     }).then(res => {
//         console.log(res)
//         if(res.status == 200){
//             console.log('Login Successful you can proceed to the next page')
//         }
//         alert('You fucked up somewhere')
//     }).catch(error => {
//         console.log(error);
//     })
// }