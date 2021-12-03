db.getSiblingDB("$external").runCommand(
    {
        createUser: "CN=scraper",
        roles: [
            {role: "readWrite", db: "covid_stat"},
            {role: "readWrite", db: "covid_stat_test"},
        ],
        writeConcern: {w: "majority", wtimeout: 5000}
    }
)
db.getSiblingDB("$external").runCommand(
    {
        createUser: "CN=dashboard",
        roles: [
            {role: "read", db: "covid_stat"},
        ]
    }
)