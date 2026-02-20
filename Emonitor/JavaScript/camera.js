const video = document.getElementById("video");
const canvas = document.createElement("canvas");
const ctx = canvas.getContext("2d");

async function startCamera() {

    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;
    } catch (error) {
        
    }

    const { ipcRenderer } = require('electron');
        
    document.getElementById('sendPython').addEventListener('click', () => {
        const dataToSend = { image: captureFrame() };
        ipcRenderer.send('sendPython', dataToSend);
    });
    
    ipcRenderer.on('from-python', (event, response) => {
        document.getElementById('mainStats').innerHTML = `
        <div class = 'statRow'>
            <div class = 'statTime'>
                ${response.time}
            </div>

            <div class = 'statMess'>
                ${response.message}
            </div>
        </div>` + document.getElementById('mainStats').innerHTML;
    });

}

function captureFrame() {            
    const scaleWidth = video.videoWidth;
    const scaleHeight = video.videoHeight;

    canvas.width = scaleWidth;
    canvas.height = scaleHeight;

    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
    const pixels = imageData.data;

    let rgbMatrix = [];
    for (let y = 0; y < canvas.height; y++) {
        let row = [];
        for (let x = 0; x < canvas.width; x++) {
            let i = (y * canvas.width + x) * 4;
            let r = pixels[i];
            let g = pixels[i + 1];
            let b = pixels[i + 2];
            row.push([r, g, b]);
        }
        rgbMatrix.push(row);
    }

    return rgbMatrix;
}



startCamera();