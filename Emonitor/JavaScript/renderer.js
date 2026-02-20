const { ipcRenderer } = require('electron');

function goToStatistics() {
    document.getElementById('mainSide').style.display = 'none';
    document.getElementById('home').className = 'sideButton';

    document.getElementById('statisticsSide').style.display = 'block';
    document.getElementById('showStatistics').className = 'sideButtonClicked';
    
}

function goToHome() {
    document.getElementById('statisticsSide').style.display = 'none';
    document.getElementById('showStatistics').className = 'sideButton';

    document.getElementById('mainSide').style.display = 'block';
    document.getElementById('home').className = 'sideButtonClicked';
}
