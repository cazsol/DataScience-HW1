import requests
import matplotlib as pp
import numpy as np
from BS4 import BeautifulSoup
url = "https://www.netmarketshare.com/operating-system-market-share.aspx?qprid=9&qpcustomb=1&qpsp=2007&qpnp=1&qptimeframe=Y"
H = requests.get(url)
soup = BeautifulSoup(H.text)
