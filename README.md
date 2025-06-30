# Sunned - A PV supervisor Poller script

Sunned - A PVS Poller Script

This is a Python script that I used to poll the SunPower PVS6 to get data from the panels.
It will then take this data polled, insert it into a database and can output the data into CSV files.

Note: This script does not get PAST history from SunPower.  It can only save the data the is returned from polling the PVS.

## What it can do
* Gather JSON from the local PVS API (/cgi-bin/dl_cgi?Command=DeviceList), parse it by device, and then insert into a target DB to get history
  * You can then use this DB with visualization tools like Grafana.
* Export the data into CSV files based on SQL queries in a given folder
  * For those that like using CSV files and want to see the history without needing to query their DB

## Usage
  ````
  python Sunned.py --config ./config/config.ini
  ````

## Prerequsites
* Proxy setup to your PVS on your local network
* Python 3.11+
* SQLite3 / PostreSQL 17

## Setup
1. If you haven't already, install Python 3.11+. 
2. Once complete, run the following to set up packages
    ````
    pip install -r requirements.txt
    ````
3. DB Setup
   1. By default, the script will create a sqlite3 database to use for itself.
   2. If you already have a postgreSQL database...
      1. Run ./config/create-solar_generation.sql to create the necessary table the script will be using.
      2. Be sure to grant the appropriate rights to the user you want the script to use
   
4. Modify the config file (./config/config.ini)
   1. DB_CONFIG section
      1. connection_string - connection string of DB to use.  You can leave this alone for sqlite3.
      2. username - username to use for connecting to DB (PostgreSQL only)
      3. password - password to use for connecting to DB (PostgreSQL only)
   2. API_CONFIG section
      1. api_hostname - The IP address/hostname that is used to call the PVS api.  This is the proxy that was setup or the wifi hotspot ip address.
      2. api_port - The port that is used to call the PVS api.
      3. deviceList_endpoint - The "famous" deviceList api call.  Leave alone, but I left this configurable in case you have this pointed to something else
   3. POLLER_CONFIG section
      1. timezone - timezone that you want the reporting timestamps to use.  Defaults to EST.  For values to use,  refer to the "TZ Identifiers" [this list](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones).
      2. output_response_to_console - set true if you want the script to output the api response to console
      3. output_response_to_file - set true to output api response to a file (will be yyyymmdd-hhmmss.json in root)
      4. export_sql_queries_results_to_file - set true to output results from sql queries in ./sqlQueries to a csv file
      5. sql_query_folder - directory where sql queries to run are located
      6. export_sql_query_results_folder - director to export sql query results
   
## Where is the data saved if I'm using sqlite?
If you are using sqlite3, all the solar data will be saved to the pvs_metrics.db file in the root folder.  

You will want to backup this file as it will hold the data everytime you run this script.