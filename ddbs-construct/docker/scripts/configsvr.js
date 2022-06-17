let privateIP = "192.168.101.165"

rs.initiate({
    _id: "cfgrs",
    configsvr: true,
    members: [
        { _id: 0, host: privateIP + ":27600" },
        { _id: 1, host: privateIP + ":27601" },
    ],
});
