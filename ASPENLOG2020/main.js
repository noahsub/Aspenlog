const path = require('path');
const { app, BrowserWindow } = require('electron');

const { ipcMain } = require('electron');

let token;

ipcMain.on('token', (event, arg) => {
    token = arg;
});


function createMainWindow() {
    const mainWindow = new BrowserWindow({
        title: 'ASPENLOG2020',
        width: 1280,
        height: 720,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
            contextIsolation: true,
            enableRemoteModule: false,
            nodeIntegration: false,
            worldSafeExecuteJavaScript: true,
        },
    });

    // Remove menu bar
    mainWindow.setMenuBarVisibility(false);

    // Load a webpage without scroll bar
    // mainWindow.loadURL('https://www.seeda.ca/').then(() => {
    //     mainWindow.webContents.insertCSS(`
    //         ::-webkit-scrollbar {
    //             display: none;
    //         }
    //     `);
    // });

    mainWindow.loadFile(path.join(__dirname, './renderer/login.html'));

    mainWindow.webContents.openDevTools()
}

app.whenReady().then(() => {
   createMainWindow();
});

try {
    require('electron-reloader')(module)
} catch (_) {}