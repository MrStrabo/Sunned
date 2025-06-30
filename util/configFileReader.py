import configparser

class ConfigFileReader:
    def __init__(self, config_file_path):
        self.configFilePath = config_file_path
        self.config = configparser.ConfigParser()
        self.config.read(self.configFilePath)

    def getConfig(self, configType):
        return self.config[configType]

