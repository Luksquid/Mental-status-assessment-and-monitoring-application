const { app, BrowserWindow, ipcMain } = require('electron');
const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

let mainWindow;

app.whenReady().then(() => {
  mainWindow = new BrowserWindow({
    width: 1280,
    height: 720,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
    },
  });
  
  mainWindow.setMenuBarVisibility(false);
  
  mainWindow.loadFile('index.html');

  ipcMain.on('sendPython', (event, data) => {
    const pythonPath = path.join(__dirname, './venv', 'Scripts', 'python.exe');
    const scriptPath = path.join(__dirname, './pythonFiles/predict.py');

    const pythonProcess = spawn(pythonPath, [scriptPath]);

    pythonProcess.stdin.write(JSON.stringify(data));
    pythonProcess.stdin.end();

    pythonProcess.stdout.on('data', (data) => {

      try {
        const parsedData = JSON.parse(data.toString());
        event.reply('from-python', parsedData);
      } 
      catch (error) {
        console.error('Błąd parsowania JSON:', error);
      }
    });

    pythonProcess.stderr.on('data', (data) => {
      console.error('Błąd Pythona: ', data.toString());
    });
  });
});


ipcMain.on('makePlots', () => {
  const pythonPath = path.join(__dirname, './venv', 'Scripts', 'python.exe'); 
  const scriptPath = path.join(__dirname, './pythonFiles/makeStats.py');

  const pythonProcess = spawn(pythonPath, [scriptPath]);

  pythonProcess.stderr.on('data', (data) => {
      console.error('Błąd Pythona: ', data.toString());
  });

});

ipcMain.on('report', () => {
  const pythonPath = path.join(__dirname, './venv', 'Scripts', 'python.exe'); 
  const scriptPath = path.join(__dirname, './pythonFiles/report.py');

  const pythonProcess = spawn(pythonPath, [scriptPath]);

  pythonProcess.stderr.on('data', (data) => {
      console.error('Błąd Pythona: ', data.toString());
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});
