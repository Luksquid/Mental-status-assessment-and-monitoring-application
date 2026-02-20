let isRunning = false; 
let intervalId;

function runLoop() {
    document.getElementById('sendPython').click();
}

document.getElementById("startStop").addEventListener("click", function () {
    if (!isRunning) {
        isRunning = true;
        intervalId = setInterval(runLoop, 1000);
        this.textContent = "Stop"; 
        document.getElementById('startStop').style.backgroundColor = 'red';
        document.getElementById('video').style.display = 'block';
    } else {
        isRunning = false;
        this.textContent = "Start"; 
        document.getElementById('startStop').style.backgroundColor = 'green';
        document.getElementById('video').style.display = 'none';
        clearInterval(intervalId)

        setTimeout(() => {
            ipcRenderer.send('makePlots');
        }, 10000);
    }
});