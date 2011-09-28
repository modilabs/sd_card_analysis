
import sqlite3, sys
from datetime import datetime
from datetime import timedelta
import matplotlib.pyplot as plt
import matplotlib.dates
import numpy

# specify database here
db = 'test.db'
#db = './data/ml06/ml06.db'

'''
this method pulls all data from the database for
<circuit> in the range specified by the timeStart
and timeEnd datetime objects
'''
def getRawDataForCircuit(circuit,
                         timeStart=datetime(2011,6,1),
                         timeEnd=datetime(2011,6,3)):

    con = sqlite3.connect(db, detect_types = sqlite3.PARSE_COLNAMES)
    sql = """select timestamp as 'ts [timestamp]',watthours_today,credit,watts
             from logs where circuitid=%s and timestamp between '%s' and '%s'
             order by timestamp asc;""" % (circuit, timeStart, timeEnd)

    dates = []
    data = []
    credit = []
    watts = []

    for i, row in enumerate(con.execute(sql)):
        dates.append(row[0])
        data.append(row[1])
        credit.append(row[2])
        watts.append(row[3])
    con.close()

    # what if no data?

    dates = numpy.array(dates)
    data = numpy.array(data)
    credit = numpy.array(credit)
    watts = numpy.array(watts)
    return dates, data, credit, watts

'''
this method reduces the amount of data returned from the database by
a simple dropping of samples.  every downsample-th sample is returned
by the function
'''
def getDecimatedDataForCircuit(circuit,
                               timeStart,
                               timeEnd,
                               downsample=20 * 20):
    dates, data, credit, watts = getRawDataForCircuit(circuit, timeStart, timeEnd)

    index = range(0, data.shape[0], downsample)
    dates = dates[index]
    data = data[index]
    credit = credit[index]
    watts = watts[index]
    return dates, data, credit, watts

'''
simple plotting of watthour samples for circuit over a specified date range
'''
def graphDailyWattHours(circuit,
                        timeStart=datetime(2011, 8, 1),
                        timeEnd=datetime(2011, 9, 6),
                        plot_file_name=None):

    dates, data, credit, watts = getRawDataForCircuit(circuit, timeStart, timeEnd)
    #dates, data, credit, watts = getDecimatedDataForCircuit(circuit, timeStart, timeEnd)
    dates = matplotlib.dates.date2num(dates)

    print "plotting"
    fig = plt.figure()
    ax = fig.add_axes((0.1,0.2,0.8,0.7))
    ax.plot_date(dates, data, 'kx')
    #ax.plot_date(dates, credit, 'kx')
    ax.set_ylabel("Watt Hours")
    #ax.set_ylabel("Credit")
    ax.set_xlabel("Time (hours passed)")
    ax.set_title(db + "\nCircuit %s between %s and %s" % (circuit, timeStart, timeEnd))
    fig.autofmt_xdate()
    if plot_file_name==None:
        plot_file_name = db + '_' + str(circuit) + '.pdf'
    fig.savefig(plot_file_name)

    print "done."

#dates, data, credit, watts = getRawDataForCircuit(1)
graphDailyWattHours(1)