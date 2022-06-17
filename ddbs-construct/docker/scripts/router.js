let privateIP = "192.168.101.165";

// add shards into
sh.addShard("shard0/" + privateIP + ":27700");
sh.addShard("shardrep/" + privateIP + ":27701," + privateIP + ":27710");
sh.addShard("shard1/" + privateIP + ":27711");

// add tag of shards
sh.addShardTag("shard0", "DBMS1");
sh.addShardTag("shard1", "DBMS2");
sh.addShardTag("shardrep", "DBMS12");

// create new database
db = db.getSiblingDB("test");
sh.enableSharding("test");

// config shard data collection
sh.shardCollection("test.user_beijing", { uid: 1 });
sh.addTagRange("test.user_beijing", { uid: MinKey }, { uid: MaxKey }, "DBMS1");

sh.shardCollection("test.user_hong_kong", { uid: 1 });
sh.addTagRange(
    "test.user_hong_kong",
    { uid: MinKey },
    { uid: MaxKey },
    "DBMS2"
);

sh.shardCollection("test.article_science", { aid: 1 });
sh.addTagRange(
    "test.article_science",
    { aid: MinKey },
    { aid: MaxKey },
    "DBMS12"
);

sh.shardCollection("test.article_tech", { aid: 1 });
sh.addTagRange("test.article_tech", { aid: MinKey }, { aid: MaxKey }, "DBMS2");

sh.shardCollection("test.read_beijing", { id: 1 });
sh.addTagRange("test.read_beijing", { id: MinKey }, { id: MaxKey }, "DBMS1");

sh.shardCollection("test.read_hong_kong", { id: 1 });
sh.addTagRange("test.read_hong_kong", { id: MinKey }, { id: MaxKey }, "DBMS2");

sh.shardCollection("test.be_read_science", { brid: 1 });
sh.addTagRange(
    "test.be_read_science",
    { brid: MinKey },
    { brid: MaxKey },
    "DBMS12"
);

sh.shardCollection("test.be_read_tech", { brid: 1 });
sh.addTagRange(
    "test.be_read_tech",
    { brid: MinKey },
    { brid: MaxKey },
    "DBMS2"
);

sh.shardCollection("test.popular_rank_daily", { prid: 1 });
sh.addTagRange(
    "test.popular_rank_daily",
    { prid: MinKey },
    { prid: MaxKey },
    "DBMS1"
);

sh.shardCollection("test.popular_rank_weekly", { prid: 1 });
sh.addTagRange(
    "test.popular_rank_weekly",
    { prid: MinKey },
    { prid: MaxKey },
    "DBMS2"
);

sh.shardCollection("test.popular_rank_monthly", { prid: 1 });
sh.addTagRange(
    "test.popular_rank_monthly",
    { prid: MinKey },
    { prid: MaxKey },
    "DBMS2"
);
