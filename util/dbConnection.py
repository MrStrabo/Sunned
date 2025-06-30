from urllib.parse import urlparse
import sqlite3, psycopg2

class DBConnection:
    def __init__(self, db_config):
        self.db_config = db_config
        #parse URL
        fullConnString = urlparse(db_config['connection_string'])
        self.__parse_connection_string(fullConnString)
        self.username = db_config['username']
        self.password = db_config['password']
        self.__checkIfDatabaseTypeIsSupported()

    def connect(self):
        match self.databaseType:
            case "sqlite":
                print("Connecting to SQLite database...")
                connection = sqlite3.connect(self.hostname)
                self.connection = connection
                self.__initSqliteTablesIfNotExist()

            case "postgresql":
                print("Connecting to PostgreSQL database...")
                connection = psycopg2.connect(database = self.database,
                                              host     = self.hostname,
                                              port     = self.port,
                                              user     = self.username,
                                              password = self.password,
                                              options  = self.options)

            case _:
                raise SystemExit("Database type not supported", self.databaseType)

        self.connection = connection
        return self.connection

    def __parse_connection_string(self, fullConnString):
        self.databaseType = fullConnString.scheme
        self.hostname = fullConnString.netloc.split(":")[0]

        if self.databaseType == "postgresql":
            self.port = fullConnString.netloc.split(":")[1]
            self.database = fullConnString.path.replace("/", "")
            self.options = fullConnString.query.replace("options=", "")

    def __checkIfDatabaseTypeIsSupported(self):
        if self.databaseType != "postgresql" and self.databaseType != "sqlite":
            raise SystemExit("**ERROR!** Database type [" + self.databaseType + "] not supported!  "
                            "Only postgresql or sqlite are supported.")

    def __initSqliteTablesIfNotExist(self):
        cur = self.connection.cursor()
        cur.execute("SELECT COUNT(*) FROM sqlite_schema WHERE type = 'table' and tbl_name = 'solar_generation'")
        result = cur.fetchall()

        if (result[0][0] == 0):
            print("sqlite3: SOLAR_GENERATION TABLE NOT FOUND")
            print("Creating SOLAR_GENERATION TABLE...")
            with open("./config/create-solar_generation.sql", "r") as sqlFile:
                createSolarGeneration = sqlFile.read()
                cur.execute(createSolarGeneration)
            print("Created SOLAR_GENERATION TABLE SUCCESS!")

            cur.close()

