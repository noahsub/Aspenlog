const path = require('path');
const {app, BrowserWindow} = require('electron');

const {ipcMain} = require('electron');
const keytar = require('keytar');

ipcMain.handle('store-token', async (event, token) =>
{
    await keytar.setPassword('ASPENLOG2020', 'TokenAccount', token);
});

ipcMain.handle('get-token', async () =>
{
    return await keytar.getPassword('ASPENLOG2020', 'TokenAccount');
});

ipcMain.handle('store-connection-address', async (event, connectionAddress) =>
{
    await keytar.setPassword('ASPENLOG2020', 'ConnectionAccount', connectionAddress);
});

ipcMain.handle('get-connection-address', async () =>
{
    return await keytar.getPassword('ASPENLOG2020', 'ConnectionAccount');
});

function createMainWindow()
{
    const mainWindow = new BrowserWindow({
        title: 'frontend',
        width: 1280,
        height: 720,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
            contextIsolation: true,
            enableRemoteModule: false,
            nodeIntegration: false,
            worldSafeExecuteJavaScript: true,
            // devTools: false,
        },
    });

    // Remove menu bar
    mainWindow.setMenuBarVisibility(false);
    mainWindow.loadFile(path.join(__dirname, './renderer/login.html'));
}

app.whenReady().then(async () =>
{
    await keytar.setPassword('ASPENLOG2020', 'ConnectionAccount', 'http://localhost:42613');
    createMainWindow();
});

try
{
    require('electron-reloader')(module)
}
catch (_)
{}