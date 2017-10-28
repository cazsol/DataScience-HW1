"""
AUTHOR: ERIK BACILIO
PURPOSE: HW1 DATA SCIENCE FOR PRODUCT MANAGEMENT
CONTENTS: HTTP REQUEST, DATA PARSER, DATAFRAME CREATION, GRAPH FOR DATAFRAME
DATE: OCTOBER 27, 2017
"""
# PLEASE MAKE SURE ALL THE LIBRARIES ARE LOADED AND INSTALLED
import requests
import matplotlib.pyplot as pp
import numpy as np
import pandas as pd
requests.packages.urllib3.disable_warnings() # DISABLE WARNINGS FROM NON TRUSTED SSL CONNECTIONS
# JUST HARCODES THE YEARS FOR THE GRAPH
lowerBound = 2007
higherBound = 2017
# LISTS TO CONTAIN THE SERIES OF MARKET SHARES
HshareiOS = []
HshareAndroid = []
# AGGREGATES EVERY OBSERVATION TO THE LISTS DEFINED ABOVE
def graph(dataFrame, ylabel=None, xlabel=None, labels=None, title=None, xmin=None,xmax=None):
    #PLOTS THE DATAFRAME
    ax1 = dataFrame.plot()
    # NAMES AXES
    pp.ylabel(ylabel)
    pp.xlabel(xlabel)
    # HANDLES LINES AND LABELS
    lines, labels = ax1.get_legend_handles_labels()
    # HANDLES LEGEND
    ax1.legend(lines, labels, loc='best', title=title)
    # HANDLES AXES LIMITS
    axes = pp.gca()
    axes.set_xlim([xmin,xmax])
    # GRAPH
    pp.show()
def aggregator(listSent,OS):
    # SEPARATE THE OBSERVATIONS IN THE LISTS
    monthlist = listSent.split(",")
    # COLLECTS THE OBSERVATIONS IN THE CORRESPONFING LIST
    for x in monthlist:
        if OS == "iOS":
            HshareiOS.append(round(float(x),4)*100)
        else:
            HshareAndroid.append(round(float(x),4)*100)
# CREATES LOOP TO MAKE THE REQUESTS FOR INFORMATION PER YEAR
def collector():
    processMonitor = 0
    for i in range(lowerBound,higherBound+1):
        url = 'https://www.netmarketshare.com/operating-system-market-share.aspx?qprid=9&qpcustomb=1&qpsp={0}&qpnp=1&qptimeframe=Y'.format(i)
        H = requests.get(url, verify=False)
        data = H.text
        # BREAKES THE TEXT OF THE RESPONSE TO MAKE IT MORE MANAGEABLE
        data = data.split("xAxis")
        data = data[1]
        data = data.split("yAxis")
        datafiltered = data[0]
        # isolates the data from the OS
        sectionStartiOS = datafiltered.find("iOS")+18
        sectionEndiOS = datafiltered.find("]",sectionStartiOS)
        sectionStartAndroid = datafiltered.find("Android")+22
        sectionEndAndroid = datafiltered.find("]", sectionStartAndroid)
        # ORGANIZE DATA TO SEND IT FOR COLLECTION
        yearlyiOSShare = datafiltered[sectionStartiOS:sectionEndiOS]
        yearlyAndroidShare = datafiltered[sectionStartAndroid:sectionEndAndroid]
        aggregator(yearlyiOSShare,"iOS")
        aggregator(yearlyAndroidShare,"Android")
        processMonitor += 1
        progress = round(processMonitor/len(range(lowerBound,higherBound+1))*100,2)
        print(str(progress)+"% progress")
def main():
    print("Script started")
    collector() # STARTS COLLECTING INFORMATION
    #CONVERTS INFORMATION INTO DATADRAMES
    d = pd.date_range(start='1/1/2007', end='09/1/2017', freq='MS')
    df = pd.DataFrame({'iOS':HshareiOS,'Android':HshareAndroid}, index=d)
    labels = ["iOS","Android"]
    # CALLS FUNCTION TO GRAPH
    graph(df,"Market share %","Timeline", labels, "Mobile/Tablet OS share",'2007-10-01','2017-09-01')
main()
