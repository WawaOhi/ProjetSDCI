const express = require('express');
const app = express();
const port = 3000
/* Add middleware that parses incoming json in req.body */
app.use(express.json());

const CODE_URL_BASE = "http://homepages.laas.fr/smedjiah/tmp/mw/"

const conf = {
    type : "",
    localIp : "",
    localPort : "",
    localName : "",
    remoteIp : "",
    remotePort : "",
    remoteName : "",
    codeURL : "",
    deviceName : "",
    sendPeriod : ""
};

const confServer = {...conf},
    confGatewayI = {...conf},
    confGatewayF = {...conf},
    confDevice = {...conf},
    confApplication = {...conf};

/* Server Config */
confServer.type = "server"
confServer.localIp = "10.0.0.1";
confServer.localPort = "8080";
confServer.localName = "srv";
confServer.codeURL = CODE_URL_BASE + "server.js";

/* Gateway Intermédiaire config */
confGatewayI.type = "gateway"
confGatewayI.localIp = "10.0.0.2";
confGatewayI.localPort = "8181";
confGatewayI.localName = "gi";
confGatewayI.remoteIp = "10.0.0.1";
confGatewayI.remotePort = "8080";
confGatewayI.remoteName = "srv";
confGatewayI.codeURL = CODE_URL_BASE + "gateway.js";

/* Gateway F config */
confGatewayF.type = "gateway"
confGatewayF.localPort = "8282";
confGatewayF.remoteIp = "10.0.0.2";
confGatewayF.remotePort = "8181";
confGatewayF.remoteName = "gi";
confGatewayF.codeURL = CODE_URL_BASE + "gateway.js";

/* Device Config */
confDevice.type = "device"
confDevice.codeURL = CODE_URL_BASE + "device.js";
confDevice.sendPeriod = "3000";

/* Application Config*/
confApplication.type = "application"
confApplication.remotePort = "8080";
confApplication.codeURL = CODE_URL_BASE + "application.js";
confApplication.deviceName = "app";
confApplication.sendPeriod = "5000";

app.get('/getConf/:containerName', (req, res) => {
    const name = req.params.containerName;
    console.log(`Detected Req Cont Name : ${name}`)
    switch (name) {
        case 'Server':
            res.json(confServer);
            res.status(200);
            break
        case 'GatewayI':
            res.json(confGatewayI);
            res.status(200);
            break
        case 'GatewayF1':
            confGatewayF.localIp = "10.0.0.3";
            confGatewayF.localName = "gf1";
            res.json(confGatewayF);
            res.status(200);
            break
        case 'GatewayF2':
            confGatewayF.localIp = "10.0.0.4";
            confGatewayF.localName = "gf2";
            res.json(confGatewayF);
            res.status(200);
            break
        case 'GatewayF3':
            confGatewayF.localIp = "10.0.0.5";
            confGatewayF.localName = "gf3";
            res.json(confGatewayF);
            res.status(200);
            break
        case 'Device1_1':
            confDevice.localIp = "10.0.0.6";
            confDevice.localPort = "9001";
            confDevice.localName = "device1_1";
            confDevice.remoteIp = "10.0.0.3";
            confDevice.remotePort = "8282";
            confDevice.remoteName = "gf1";
            res.json(confDevice);
            res.status(200);
            break
        case 'Device1_2':
            confDevice.localIp = "10.0.0.7";
            confDevice.localPort = "9001";
            confDevice.localName = "device1_2";
            confDevice.remoteIp = "10.0.0.3";
            confDevice.remotePort = "8282";
            confDevice.remoteName = "gf1";
            res.json(confDevice);
            res.status(200);
            break
        case 'Device1_3':
            confDevice.localIp = "10.0.0.8";
            confDevice.localPort = "9001";
            confDevice.localName = "device1_3";
            confDevice.remoteIp = "10.0.0.3";
            confDevice.remotePort = "8282";
            confDevice.remoteName = "gf1";
            res.json(confDevice);
            res.status(200);
            break
        case 'Device2_1':
            confDevice.localIp = "10.0.0.9";
            confDevice.localPort = "9001";
            confDevice.localName = "device2_1";
            confDevice.remoteIp = "10.0.0.4";
            confDevice.remotePort = "8282";
            confDevice.remoteName = "gf2";
            res.json(confDevice);
            res.status(200);
            break
        case 'Device3_1':
            confDevice.localIp = "10.0.0.10";
            confDevice.localPort = "9001";
            confDevice.localName = "device3_1";
            confDevice.remoteIp = "10.0.0.5";
            confDevice.remotePort = "8282";
            confDevice.remoteName = "gf3";
            res.json(confDevice);
            res.status(200);
            break
        case 'Application':
            res.json(confApplication);
            res.status(200);
            break
        default :
            res.status(404);
    }
    res.send();
})

app.listen(port, () => {
  console.log(`Metadata server listening on port ${port}`)
})
