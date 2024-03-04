// This file is used to expose the electron API to the window object
const {contextBridge, ipcRenderer} = require('electron');

contextBridge.exposeInMainWorld(
    'api', {
        invoke: (channel, data) => ipcRenderer.invoke(channel, data)
    }
);
