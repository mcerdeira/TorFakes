import StringIO
import socket
import urllib

import socks  # SocksiPy module
import stem.process
import random

from stem.util import term

# Based on: http://dev.maxmind.com/geoip/legacy/codes/iso3166/
# Test which countries workss
country_codes = ['ru', 'nl', 'ar', 'br', 'ua', 'us', 'tr', 'ca', 'au', 'gr', 'es', 'fr', 'it', 'gb', 'de', 'se', 'pt', 'za', 'mx', 'jp', 'hr', 'ch', 'no']

urls = ["HERE YOU INSERT THE URLS LIST"]

for i in range(500): #500 is just a magic number, replace as you wish
    SOCKS_PORT = 9150
    
    print str("##############################################################################")
    print str(i)
    print str("##############################################################################")

    # Set socks proxy and wrap the urllib module
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, '127.0.0.1', SOCKS_PORT)
    socket.socket = socks.socksocket

    # Perform DNS resolution through the socket

    def getaddrinfo(*args):
      return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (args[0], args[1]))]

    socket.getaddrinfo = getaddrinfo


    def query(url):
      """
      Uses urllib to fetch a site using SocksiPy for Tor over the SOCKS_PORT.
      """

      try:
        return urllib.urlopen(url).read()
      except:
        return "Unable to reach %s" % url

    # Start an instance of tor configured to only exit through Russia. This prints
    # tor's bootstrap information as it starts. Note that this likely will not
    # work if you have another tor instance running.

    def print_bootstrap_lines(line):
        print term.format(line, term.Color.BLUE)
    
    print term.format("Starting Tor:\n", term.Attr.BOLD)

    country = random.choice(country_codes)
    print str("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    print "Random country: " + country
    print str("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    
    tor_process = stem.process.launch_tor_with_config(
      config = {
        'DataDirectory': 'C:\\Users\\<user>\\Documents\\Tor Browser\\Data\\Tor',
        'DirReqStatistics': '0',
        'GeoIPFile': 'C:\\Users\\<user>\\Documents\\Tor Browser\\Data\\Tor\\geoip',              
        'ControlPort': '9151',
        'CookieAuthentication': '1',        
        'HashedControlPassword': 'YOU CAN GET THIS DEBUGING tor.exe command line parameters',       
        'SocksPort': str(SOCKS_PORT),
        'ExitNodes': '{' + country.lower() + '}'
      },
      init_msg_handler = print_bootstrap_lines,
      take_ownership = True,
    )

    #print term.format("\nChecking our endpoint:\n", term.Attr.BOLD)
    #print term.format(query("https://www.atagar.com/echo.php"), term.Color.BLUE)
        
    url = random.choice(urls)
    print "Querying... " + url
    query(url)
    print "Done!"
    
    tor_process.kill()  # stops tor