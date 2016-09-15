#!/usr/bin/env python

import requests
import getpass
import bs4
import re
import time
import sys

################################################################################
#####                         LOGIN PROCESS                                #####
################################################################################
#   1. POST login data to https://www.jumbocash.net/login.php and parse the
#      skey (session key).
#   2. GET intermediate "Please wait while we access your account." page.
#      For some reason the login process fails if this is skipped.
#   3. GET login-check.php xml page, parse out value of <message> tag which
#      indicates whether or not the process is complete. Continue requesting
#      the page after pausing for .3 seconds until the response indicates a
#      successful login or 15 attempts have been made.
#   4. GET final (index.php) page, parse JumboCash and meal swipe balances.


##############################      PART 1      ################################

CID     = 233
URL     = "https://www.jumbocash.net"
tuftsid = raw_input('Tufts ID #: ')
pw      = getpass.getpass()

data = {'cid': CID, 'save': 1, 'loginphrase' : tuftsid, 'password': pw}
res  = requests.post(URL + "/login.php", data, allow_redirects=False)
soup = bs4.BeautifulSoup(res.text, "html.parser")
pattern = re.compile(r'skey=([0-9a-z]*)&')
skey = re.search(pattern, soup.script.string).group(1)


##############################      PART 2      ################################

payload = {'skey': skey, 'cid': CID, 'fullscreen': 1, 'wason': None}
requests.get(URL + "/login.php", params=payload)


##############################      PART 3      ################################

def getStatus():
    """Parse server status and return status code:
       1:  server is ready 
       0:  server is not ready
       -1: server error"""
    res = requests.get(URL + "/login-check.php", params={'skey': skey})
    soup = bs4.BeautifulSoup(res.text, "html.parser")
    return int(soup.message.text)

serverStatus = 0
counter = 0
while serverStatus != 1:
    serverStatus = getStatus()
    if serverStatus == -1:
        sys.stderr.write("Server error")
        sys.exit()
    counter += 1
    if counter >= 15:
        sys.stderr.write("Checked login 15 times without success.")
        sys.exit()
    time.sleep(0.3)


##############################      PART 4      ################################

res = requests.get(URL + '/index.php', params={'skey': skey, 'cid': CID})
soup = bs4.BeautifulSoup(res.text, "html.parser")
jumbocash, swipes = map(lambda t: t.th.findNext().text, soup.findAll('tfoot'))

print 'Remaining Swipes: {}'.format(swipes)
print 'JumboCash Balance: ${}'.format(jumbocash)
