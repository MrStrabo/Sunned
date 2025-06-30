#configFileReader unit tests
import configparser

import pytest

from util.configFileReader import ConfigFileReader

class TestConfigFileReader:
    def test_ConfigFileReaderReadsConfigfileAndHasExpectedValues(self):
        configFileReader = ConfigFileReader("fakeConfigFile.ini")

        dbConfig = configFileReader.getConfig("DB_CONFIG")
        assert dbConfig is not None
        assert dbConfig.keys().__len__() == 4
        assert dbConfig["connection_string"] == "postgresql://123.211.11.111:5432/metrics?options=-csearch_path=hq,public"
        assert dbConfig["username"] == "FAKE_USER"
        assert dbConfig["password"] == "FAKE_PW"
        assert dbConfig["self_register"] == "true"

        apiConfig = configFileReader.getConfig("API_CONFIG")
        assert apiConfig is not None
        assert apiConfig.keys().__len__() == 4
        assert apiConfig["api_hostname"] == "fake_hostname"
        assert apiConfig["api_port"] == "9090"
        assert apiConfig["deviceList_endpoint"] == "/cgi-bin/dl_cgi?Command=DeviceList"
        assert apiConfig["panelLayout_endpoint"] == "/cgi-bin/dl_cgi?Command=Layout"

        pollerConfig = configFileReader.getConfig("POLLER_CONFIG")
        assert pollerConfig is not None
        assert pollerConfig.__len__() == 5
        assert pollerConfig["output_response_to_console"] == "false"
        assert pollerConfig["output_response_to_file"] == "true"
        assert pollerConfig["export_sql_queries_to_file"] == "true"
        assert pollerConfig["sql_query_folder"] == "./sqlQueries"
        assert pollerConfig["export_folder"] == "./reports"


    def test_ConfigFileReaderReadsConfigFileAndThrowsKeyErrorOnBadType(self):
        with pytest.raises(KeyError) as actualKeyError:
            configFileReader = ConfigFileReader("fakeConfigFile.ini")
            configFileReader.getConfig("bad_type")

        assert actualKeyError.type is KeyError