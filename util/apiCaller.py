#A generic class that uses requests and the apiConfig to make calls and returns the results
# the ApiConfig object that is passed should contain api_hostname, api_port
# For endpoints, it should have values in the apiConfig with names of this format {endpoint_name}_endpoint

import requests, validators

class ApiCaller:
    def __init__(self, apiConfig):
        self.apiConfig = apiConfig
        baseURL = f"http://{apiConfig['api_hostname']}:{apiConfig['api_port']}"
        if self.__validateURL(baseURL):
            self.baseURL = baseURL
        else:
            raise SystemExit("**ERROR!** URL [" + self.baseURL + "] not valid!  ")

    def fetchGetJSON(self, endpointName):
        getJSONRequest = requests.get(self.getFullEndpointURL(endpointName))
        return getJSONRequest.json()


    def getFullEndpointURL(self, endpointName):
        return self.baseURL + self.apiConfig[f"{endpointName}_endpoint"]


    def __validateURL(self, url):
        return validators.url(url)
