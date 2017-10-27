import requests
import matplotlib as pp
import numpy as np
from bs4 import BeautifulSoup
requests.packages.urllib3.disable_warnings()
lowerBound = 2007
higherBound = 2017
container = []
for i in range(lowerBound,higherBound+1):
    url = 'https://www.netmarketshare.com/operating-system-market-share.aspx?qprid=9&qpcustomb=1&qpsp={0}&qpnp=1&qptimeframe=Y'.format(i)
    H = requests.get(url, verify=False)
    soup = H.text
    #soup = BeautifulSoup(H.text)
    soup = soup.split("xAxis")
    data = soup[1]
    print(data)
    print("####################################################################################################")
