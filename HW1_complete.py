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
def graph(dataFrame, ylabel=None, xlabel=None, labels=None, title=None):
    #pp.plot(dataFrame, label=labels)
    ax1 = dataFrame.plot()
    pp.ylabel(ylabel)
    pp.xlabel(xlabel)
    lines, labels = ax1.get_legend_handles_labels()
    ax1.legend(lines, labels, loc='best', title=title)
    axes = pp.gca()
    axes.set_xlim(["2007-10-01","2017-09-01"])
    #axes.set_ylim([0,100])
    #ax1.legend(lines[:2], labels[:2], loc='best')
    #ax = pp.subplot(2, 1, 1)
    #pp.legend(loc="upper left", bbox_to_anchor=[0, 1],
    #    ncol=2, shadow=True, title="Legend", fancybox=True, label=labels)
    #ax.get_legend().get_title().set_color("red")
    pp.show()
def aggregator(listSent,OS):
    monthlist = listSent.split(",")
    for x in monthlist:
        if OS == "iOS":
            HshareiOS.append(round(float(x),4)*100)
        else:
            HshareAndroid.append(round(float(x),4)*100)
# CREATES LOOP TO MAKE THE REQUESTS FOR INFORMATION PER YEAR
def collector():
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
def main():
    collector()
    #matrix = np.matrix(HshareiOS,HshareAndroid)
    #df = pd.DataFrame(data=matrix)
    d = pd.date_range(start='1/1/2007', end='09/1/2017', freq='MS')
    df = pd.DataFrame({'iOS':HshareiOS,'Android':HshareAndroid}, index=d)
    labels = ["iOS","Android"]
    graph(df,"Market share %","Year", labels, "Market share")
"""
THIS IS NOT THE FINAL DRAFT i MESSED UP
"""
main()
