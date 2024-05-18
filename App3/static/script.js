// static/script.js
const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const imageData = document.getElementById('image-data');
const context = canvas.getContext('2d');

navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        video.srcObject = stream;
    })
    .catch(err => {
        console.error("Error accessing the camera: ", err);
    });

document.getElementById('capture').addEventListener('click', () => {
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    const dataURL = canvas.toDataURL('image/png');
    imageData.value = dataURL;
    canvas.style.display = 'block';
});
