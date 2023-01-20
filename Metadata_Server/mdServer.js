const express = require('express');
const app = express();
const port = 3000
/* Add middleware that parses incoming json in req.body */
app.use(express.json());

const CODE_URL_BASE = "http://homepages.laas.fr/smedjiah/tmp/mw/"

const conf = {
    type : "",
    localIp : "127.0.0.1",
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
    confGatewayF1 = {...conf},
    confGatewayF2 = {...conf},
    confGatewayF3 = {...conf},
    confDevice = {...conf},
    confApplication = {...conf};

/* Server Config */
confServer.type = "server"
confServer.localPort = "8080";
confServer.localName = "srv";
confServer.codeURL = CODE_URL_BASE + "server.js";
/* Gateway Intermédiaire config */
confGatewayI.type = "gateway"
confGatewayI.localPort = "8181";
confGatewayI.localName = "gwi";
confGatewayI.remoteIp = confGatewayI.localIp;
confGatewayI.remotePort = "8080";
confGatewayI.remoteName = "srv";
confGatewayI.codeURL = CODE_URL_BASE + "gateway.js";
/* Gateway F1 config */
confGatewayF1.type = "gateway"
confGatewayF1.localPort = "8282";
confGatewayF1.localName = "gwf1";
confGatewayF1.remoteIp = "127.0.0.1";
confGatewayF1.remotePort = "8181";
confGatewayF1.remoteName = "gwi";
confGatewayF1.codeURL = CODE_URL_BASE + "gateway.js";
/* Gateway F2 config */
confGatewayF2.type = "gateway"
confGatewayF2.localPort = "8282";
confGatewayF2.localName = "gwf2";
confGatewayF2.remoteIp = "127.0.0.1";
confGatewayF2.remotePort = "8181";
confGatewayF2.remoteName = "gwi";
confGatewayF2.codeURL = CODE_URL_BASE + "gateway.js";
/* Gateway F3 config */
confGatewayF3.type = "gateway"
confGatewayF3.localPort = "8282";
confGatewayF3.localName = "gwf3";
confGatewayF3.remoteIp = "127.0.0.1";
confGatewayF3.remotePort = "8181";
confGatewayF3.remoteName = "gwi";
confGatewayF3.codeURL = CODE_URL_BASE + "gateway.js";
/* Device Config */
confDevice.type = "device"
confDevice.localPort = "9001";
confDevice.localName = "dev1";
confDevice.remoteIp = "127.0.0.1";
confDevice.remotePort = "8282";
confDevice.remoteName = "gwf1";
confDevice.codeURL = CODE_URL_BASE + "device.js";
confDevice.sendPeriod = "3000";
/* Application Config*/
confApplication.type = "application"
confApplication.remotePort = "8080";
confApplication.codeURL = CODE_URL_BASE + "application.js";
confApplication.deviceName = "dev1";
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
            res.json(confGatewayF1);
            res.status(200);
            break
        case 'Device':
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
