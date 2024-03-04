////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// IMPORTS
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

const path = require('path');
const {app, BrowserWindow} = require('electron');
const {ipcMain} = require('electron');
const keytar = require('keytar');
const fs = require('fs');
const os = require('os');

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// APPLICATION GLOBALS
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// Function to store the token
ipcMain.handle('store-token', async (event, token) =>
{
    await keytar.setPassword('ASPENLOG2020', 'TokenAccount', token);
});

// Function to retrieve the token
ipcMain.handle('get-token', async () =>
{
    return await keytar.getPassword('ASPENLOG2020', 'TokenAccount');
});

// Function to store the connection address and port
ipcMain.handle('store-connection-address', async (event, connectionAddress) =>
{
    await keytar.setPassword('ASPENLOG2020', 'ConnectionAccount', connectionAddress);
});

// Function to retrieve the connection address and port
ipcMain.handle('get-connection-address', async () =>
{
    return await keytar.getPassword('ASPENLOG2020', 'ConnectionAccount');
});

// Function to download files
ipcMain.handle('download', (event, {data, filename}) =>
{
    // Convert Uint8Array to Buffer
    const buffer = Buffer.from(data);
    // Get user's download directory
    const downloadDir = path.join(os.homedir(), 'Downloads');
    // Write file to user's download directory
    fs.writeFile(path.join(downloadDir, filename), buffer, (err) =>
    {
        if (err)
        {
            console.error(err);
        }
        else
        {
            console.log('File downloaded successfully');
        }
    });
})

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// START APPLICATION
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

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