'''
Created on 21 apr. 2018

@author: AntonStange
'''
import csv, sys
import datetime
from pathlib import Path
import sys

REMOVE_COLUMNS = ['columnNameA','columnNameB']
filename = sys.argv[-1]


def main():
    csvFileIn = filename
    writeToLog('Reading csv file = %s' %csvFileIn)

    csvLines = csvFileToList(csvFileIn, 'r')
    headerLine = csvLines[0]

    writeToLog('Determine what columns should be removed from the csv file')

    indexesToRemove = []
    for i in range(len(headerLine)):
        removeIt = False
        for columnToRemove in REMOVE_COLUMNS:
            if headerLine[i] == columnToRemove:
                removeIt = True
        if removeIt:
            indexesToRemove.append(i)

    indexesToRemove.sort(reverse = True)

    for index in indexesToRemove:
        writeToLog('Based on the header of the CSV file column %s will be removed' %index)

    newCsvLines = []
    for line in csvLines:
        for index in indexesToRemove:
            line.pop(index)
        newCsvLines.append(line)

    filenameOut = filename.split('.')[0] + '_OUT.' + filename.split('.')[1]
    csvFileOut = filenameOut
    writeToLog('Writing to file %s' %csvFileOut)

    with open(csvFileOut, 'w', newline='\n') as csvfile:
        csvWriter = csv.writer(csvfile, delimiter=',',quotechar='"',quoting=csv.QUOTE_ALL, lineterminator="\n")
        for line in newCsvLines:
            csvWriter.writerow(line)

    writeToLog('Done!')


def csvFileToList(fileName, readType):
    csvList = []
    file = Path(fileName)
    if file.is_file():   # file exists
        with open(fileName, readType) as f:
            try:
                reader = csv.reader(f)
                for row in reader:
                    csvList.append(row)
            except csv.Error as e:
                writeToLog(str(e))
                sys.exit('file %s, line %d: %s' % (fileName, reader.line_num, e))
    else:
        writeToLog('File does not exist')
    return csvList


def writeToLog(logValue):
    logLine = (str(datetime.datetime.now()) + ': ' + logValue)
    writeLineToFile('logging.log', logLine)
    print(logLine)


def writeLineToFile(fileNameOut, appendLine):
    f = open(fileNameOut,'a')
    f.write(appendLine+'\n')


if __name__ == '__main__':
    main()
