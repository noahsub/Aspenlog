const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld(
    'api', {
        sendToken: (token) => ipcRenderer.send('token', token),
        receiveToken: (func) => ipcRenderer.on('token', (event, ...args) => func(...args))
    }
);
