var video = document.getElementById('video');
var captureBtn = document.getElementById('capture-btn');
var capturedImage = document.getElementById('captured-image');
var capturedImage = document.createElement('img');
var sendBtn = document.getElementById('submit-btn');
var imageHidden = document.getElementById('student_image')
var capturedImageHolder = document.getElementById('video-image-holder')
var stream;
var imageData;

const student_name = document.getElementById('student_name');
const matric_num = document.getElementById('matric_num');
const tel_num = document.getElementById('tel_num');
const email = document.getElementById('email');
const department_id = document.getElementById('department_id');

navigator.mediaDevices.getUserMedia({ video: true })
.then(function(stream) {
    video.srcObject = stream;
    video.play();
    stream = stream;
})
.catch(function(error) {
    console.error('Error accessing video stream:', error);
});


captureBtn.addEventListener('click', function() {
    var canvas = document.createElement('canvas');
    var context = canvas.getContext('2d');
    canvas.width = 320;
    canvas.height = 240;
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    imageData = canvas.toDataURL('image/png');
    var imageDataRes = imageData.replace("data:image/png;base64,", "");
    // console.log(imageDataRes);
    //console.log(imageData)
    imageHidden.value = imageDataRes;

    video.srcObject = null
    video.remove()
    video.style.display = 'none';
    captureBtn.style.display = 'none'

    capturedImage.src = imageData;
    capturedImage.style.display = 'block';
    capturedImageHolder.appendChild(capturedImage)

    // console.log(capturedImage)
});

// sendBtn.addEventListener('click', function(e) {
//     e.preventDefault()
//     console.log(student_name.value)
//     let c_student_name = student_name.value
//     let c_matric_num = matric_num.value
//     let c_tel_num = tel_num.value
//     let c_email = email.value
//     let c_department_id = department_id.value
//     if (c_student_name !== '' && c_matric_num !== '' && c_tel_num !== '' && c_department_id !== '' && c_email !== ''){
//         if (imageData) {
//           const upload = {
//               'student_name':c_student_name,
//               'matric_num':c_matric_num,
//               'tel_num':c_tel_num,
//               'email':c_email,
//               'dept_id':c_department_id,
//               'student_image':imageData
//             }
//             sendFormData(upload);
//           console.log(upload);
//         } else {
//           console.log('No image data available.');
//           alert('No image data available.')
//         }
//     } else{
//         console.log('Fill in all the required details');
//         alert('Fill in all the required details');
//     }
// });

// function sendFormData(upload) {
//     fetch('/admin/add-student',{
//         method: 'POST',
//         headers:{
//             'Content-Type': 'application/json'
//         },
//         body: JSON.stringify(upload)
//     }).then(res=>{
//         console.log(res)
//         if(res.status==200){
//            return window.location.href = '/admin/dashboard';
//         }
//         alert("Error")
//     }).catch(error=>{
//         console.log(error);
//     })
// }

