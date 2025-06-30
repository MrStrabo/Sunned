import csv, glob, os

class DBQueryResultsExporter:
    def __init__(self, dbCursor):
        self.dbCursor = dbCursor

    def exportQueriesFromDir(self, dirName, exportFolder):
        #check if export folder exists.  If not, create it
        os.mkdir(exportFolder) if not os.path.exists(exportFolder) else False

        for file in glob.glob(f"{dirName}/*.sql"):
            print("Extracting query from file: " + file)
            with open(file, "r") as sqlQuery:
                sqlQuery = sqlQuery.read()
                sqlFileBaseName = os.path.basename(file)
                targetCSVFilename = f"{exportFolder}/{sqlFileBaseName.replace('.sql', '.csv')}"
                self.exportQueryResultsToCSV(sqlQuery, targetCSVFilename)

    def exportQueryResultsToCSV(self, sqlQuery, filename):
        print(f"Exporting to file: {filename}")
        self.dbCursor.execute(sqlQuery)

        queryResults = self.dbCursor.fetchall()

        with open(filename, 'w') as csvfile:
            csvWriter = csv.writer(csvfile)

            #first row is column names
            colnames = [desc[0] for desc in self.dbCursor.description]
            csvWriter.writerow(colnames)

            #then output the rest
            csvWriter.writerows(queryResults)