let privateIP = "192.168.101.165";

rs.initiate({
    _id: "shard1",
    members: [{ _id: 1, host: privateIP + ":27711" }],
});
