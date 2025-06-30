# Script to post PVS6 payload data to database
import argparse, json
import uuid

from datetime import datetime
from zoneinfo import ZoneInfo

from util.apiCaller import ApiCaller
from util.configFileReader import ConfigFileReader
from util.dbConnection import DBConnection
from util.dbQueryResultsExporter import DBQueryResultsExporter

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--source", default="PVS", help="Source system")
parser.add_argument("-c", "--config", help="Config file")

args = parser.parse_args()
source = args.source
config = args.config

configFileReader = ConfigFileReader(config)
dbConnection = DBConnection(configFileReader.getConfig("DB_CONFIG"))
apiCaller = ApiCaller(configFileReader.getConfig("API_CONFIG"))
pollerConfig = configFileReader.getConfig("POLLER_CONFIG")

#current time
currentDatetime = datetime.now(ZoneInfo(pollerConfig["timezone"]))
currentTimestamp = currentDatetime.strftime("%Y-%m-%d %H:%M:%S %z")

#Connect to DB
conn = dbConnection.connect()
cur = conn.cursor()

#Call API
print("Calling PVS device list: " + apiCaller.getFullEndpointURL("deviceList"))
deviceListJSON = apiCaller.fetchGetJSON("deviceList")

print(deviceListJSON) if (pollerConfig["output_response_to_console"] == "true") else None

if pollerConfig["output_response_to_file"] == "true":
    responseFileName = currentDatetime.strftime("%Y%m%d-%H%M%S") + ".json"
    print("Writing PVS JSON response to file: " + responseFileName)
    with open(responseFileName, "w") as f:
        f.write(json.dumps(deviceListJSON))


print("Parsing PVS device list JSON...")
for device in deviceListJSON["devices"]:
    serial = device["SERIAL"]
    if "TYPE" in device:
        device_type = device["TYPE"]
    else:
        device_type = device['DEVICE_TYPE']

    #Craft SQL
    insertSQLPrefix = "INSERT INTO solar_generation(rowid, reporting_ts, source_system, device_type, serial_number, data_payload) VALUES"
    insertData = (str(uuid.uuid4()), currentTimestamp, source, device_type, serial, json.dumps(device))

    if dbConnection.databaseType == "sqlite":
        insertSQL = (f"{insertSQLPrefix} (?, ?, ?, ?, ?, ? )")
    else:
        insertSQL = (f"{insertSQLPrefix} (%s, %s, %s, %s, %s, %s)")

    print(f"**Inserting data for {device_type} ({serial})....")
    cur.execute(insertSQL, insertData)

#commit inserts
print("Committing records to DB...")
conn.commit()

#Generating reports using sql queries
if pollerConfig['export_sql_queries_results_to_file'] == 'true':
    print("Exporting SQL query results...")
    dbQueryResultsExporter = DBQueryResultsExporter(cur)
    dbQueryResultsExporter.exportQueriesFromDir(pollerConfig["sql_query_folder"], pollerConfig["export_sql_query_results_folder"] )

print("Closing DB...")
cur.close()
#close connection
conn.close()