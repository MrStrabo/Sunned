#configFileReader unit tests
import configparser

import pytest

from util.configFileReader import ConfigFileReader
from util.dbConnection import DBConnection


class TestDBConnection:
    def test_DBConnection_WithPostgresSQLConfig(self):
        configFileReader = ConfigFileReader("fakeConfigFile.ini")

        dbConfig = configFileReader.getConfig("DB_CONFIG")
        dbConnection = DBConnection(dbConfig)
        assert dbConnection is not None
        assert dbConnection.databaseType == "postgresql"
        assert dbConnection.database == "metrics"
        assert dbConnection.hostname == "123.211.11.111"
        assert dbConnection.port == "5432"
        assert dbConnection.username == "FAKE_USER"
        assert dbConnection.password == "FAKE_PW"
        assert dbConnection.options == "-csearch_path=hq,public"

