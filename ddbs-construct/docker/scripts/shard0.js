let privateIP = "192.168.101.165";

rs.initiate({
    _id: "shard0",
    members: [{ _id: 0, host: privateIP + ":27700" }],
});
