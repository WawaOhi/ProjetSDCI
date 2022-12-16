const express = require('express');
const app = express();
const port = 3000
/* Add middleware that parses incoming json in req.body */
app.use(express.json());

const conf = {
    localIp : "127.0.0.1",
    localPort : "",
    localName : "",
    remoteIp : "",
    remotePort : "",
    remoteName : "",
    codeURL : "http://homepages.laas.fr/smedjiah/tmp/mw/",
    deviceName : "",
    sendPeriod : ""
};

const confServer = conf,
    confGatewayI = conf,
    confGatewayF1 = conf,
    confDevice = conf,
    confApplication = conf;

/* Server Config */
confServer.localPort = "8080";
confServer.localName = "srv";
confServer.codeURL = confServer.codeURL + "server.js";
/* Gateway Intermédiaire config */
confGatewayI.localPort = "8181";
confGatewayI.localName = "gwi";
confGatewayI.remoteIp = confGatewayI.localIp;
confGatewayI.remotePort = "8080";
confGatewayI.remoteName = "srv";
confGatewayI.codeURL = confGatewayI.codeURL + "gateway.js";
/* Gateway F1 config */
confGatewayF1.localPort = "8282";
confGatewayF1.localName = "gwf1";
confGatewayF1.remoteIp = "127.0.0.1";
confGatewayF1.remotePort = "8181";
confGatewayF1.remoteName = "gwi";
confGatewayF1.codeURL = confGatewayF1 + "gateway.js";
/* Device Config */
confDevice.localPort = "9001";
confDevice.localName = "dev1";
confDevice.remoteIp = "127.0.0.1";
confDevice.remotePort = "8282";
confDevice.remoteName = "gwf1";
confDevice.codeURL = confDevice + "device.js";
confDevice.sendPeriod = "3000";
/* Application Config*/
confApplication.remotePort = "8080";
confApplication.codeURL = confApplication.codeURL + "application.js";
confApplication.deviceName = "dev1";
confApplication.sendPeriod = "5000";

app.get('/getConf/:containerName', (req, res) => {
    const name = req.params.containerName;
    switch (name) {
        case 'Server':
            res.write(confServer);
            res.status(200);
            break
        case 'GatewayI':
            res.write(confGatewayI);
            res.status(200);
            break
        case 'GatewayF1':
            res.write(confGatewayF1);
            res.status(200);
            break
        case 'Device':
            res.write(confDevice);
            res.status(200);
            break
        case 'Application':
            res.write(confApplication);
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
