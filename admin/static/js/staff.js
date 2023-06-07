var video = document.getElementById('video');
var captureBtn = document.getElementById('capture-btn');
var capturedImage = document.getElementById('captured-image');
var capturedImage = document.createElement('img');
var sendBtn = document.getElementById('submit-btn');
var imageHidden = document.getElementById('staff_image');
var capturedPicture = document.getElementById('video-image-holder')
var stream;
var imageData;

const staff_name = document.getElementById('staff_name');
const staff_reg_num = document.getElementById('staff_reg_num');
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
    imageHidden.value = imageDataRes;
    //console.log(imageData)

    video.srcObject = null
    video.remove()
    video.style.display = 'none';
    captureBtn.style.display = 'none'

    capturedImage.src = imageData;
    capturedImage.style.display = 'block';
    capturedPicture.appendChild(capturedImage)

    // console.log(capturedImage)
});

// sendBtn.addEventListener('click', function(e) {
//     e.preventDefault()
//     console.log(staff_name.value)
//     let c_staff_name = staff_name.value
//     let c_staff_reg_num = staff_reg_num.value
//     let c_tel_num = tel_num.value
//     let c_email = email.value
//     let c_department_id = department_id.value
//     if (c_staff_name !== '' && c_staff_reg_num !== '' && c_tel_num !== '' && c_department_id !== '' && c_email !== ''){
//         if (imageData) {
//           const upload = {
//               'staff_name':c_staff_name,
//               'staff_reg_num':c_staff_reg_num,
//               'tel_num':c_tel_num,
//               'email':c_email,
//               'dept_id':c_department_id,
//               'staff_image':imageData
//             }
//             sendFormData(upload);
//           console.log(upload);
//         } else {
//           console.log('No image data available.');
//           alert('No image data available.');
//         }
//     } else {
//         console.log('Fill in all the required details.')
//         alert('Fill in all the required details.')
//     }
// });

// function sendFormData(upload) {
//     fetch('/admin/add-staff',{
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