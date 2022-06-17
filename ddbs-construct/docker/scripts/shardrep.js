let privateIP = "192.168.101.165";

rs.initiate({
    _id: "shardrep",
    members: [
        { _id: 0, host: privateIP + ":27701" },
        { _id: 1, host: privateIP + ":27710" },
    ],
});
