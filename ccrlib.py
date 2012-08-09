# CCR Library for Python 3

# Imports
import json
from urllib import request

# Constants
CCR_BASE = "http://chakra-linux.org/ccr/"
CCR_RPC = CCR_BASE + "rpc.php?type="
CCR_PKG = CCR_BASE + "packages.php"
CCR_SUBMIT = CCR_BASE + "pkgsubmit.php"
ARG = "&arg="
SEARCH = CCR_RPC + "search" + ARG
INFO = CCR_RPC + "info" + ARG
MSEARCH = CCR_RPC + "msearch" + ARG
LATEST = CCR_RPC + "getlatest" + ARG

# Information Classes and Functions
def search(keyword):
  """Searches packages by keyword"""
  return json.loads(request.urlopen(SEARCH + keyword).read().decode())['results']

def info(package):
  """Returns information about a package"""
  return json.loads(request.urlopen(INFO + package).read().decode())['results']

def msearch(maintainer):
  """Searches for packages maintained by a certain maintainer"""
  return json.loads(request.urlopen(MSEARCH + maintainer).read().decode())['results'] 

def orphans():
  """Searches for orphaned packages"""
  return msearch('0');

def geturl(package, by='name'):
  """Gets the url of package by name or id."""
  if by == 'name':
    return CCR_PKG + "?ID=" + info(package)['ID']
  elif by == 'id':
    return CCR_PKG + "?ID=" + package

def getlatest(num=10):
  """Gets the info for the latest `num` CCR packages then returns as a list"""
  return json.loads(request.urlopen(LATEST + str(num)).read().decode())['results']

# File functions
def getfilesurl(package):
  """Gets the url of the source files."""
  return CCR_BASE + 'packages/' + package[:2] + '/' + package + '/'

def getfileurl(package, file):
  """Gets the url of a file in the package."""
  return getfilesurl(package) + package + '/' + file

def getpkgurl(package):
  """Gets the url of the source package."""
  return getfilesurl(package) + package + '.tar.gz'

def getpkgbuildurl(package):
  """Gets the url of the PKGBUILD."""
  return getfileurl(package, 'PKGBUILD')

def getonlinepkgbuildurl(package):
  """Gets the url of the PKGBUILD viewer online."""
  return CCR_BASE + "pkgbuild_view.php?p=" + package

def getpkg(package, destination):
  """Downloads the source package."""
  request.urlretrieve(getpkgurl(package), destination)

# Test
if __name__ == "__main__":
  r = info("ffpy")
  for key in r.keys():
    print('%s: %s' % (key, r[key]))
