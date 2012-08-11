# CCR Library for Python 3

# Imports
import json # For information functions
import redis
from urllib import request, parse, error # For contacting the CCR
from sys import exit as exitcode # For exiting
from http import cookiejar # For __init__ in CCRSession

## Not in use
#import re # For submit in CCRSession
#from functools import reduce # For printing the dictionary

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
CATEGORY_NUMS = {
                "none": 1,
                "daemons": 2,
                "devel": 3,
                "editors": 4,
                "emulators": 5,
                "games": 6,
                "gnome": 7,
                "i18n": 8,
                "kde": 9,
                "lib": 10,
                "modules": 11,
                "multimedia": 12,
                "network": 13,
                "office": 14,
                "educational": 15,
                "system": 16,
                "x11": 17,
                "utils": 18,
                "lib32": 19,
                }
EXPIRE=12000

# Pretty Print Dictionaries
def printDict(dict, indent=0, seperate='align', endwith='\n'):
  """Prints a dictionary in a readable way."""
  if seperate != 'align':
    for key in dict.keys():
      print("%s%s:%s%s" % ((" " * indent),key, seperate, dict[key]), end=endwith)
    if '\n' not in endwith:
      print('\n')
  else:
#    totalLen = len(reduce(lambda x, y: x if len(x) >= len(y) else y, dict.keys()))
    totalLen = max(map(len, dict))
    for key in dict.keys():
      seperate = ' ' * (totalLen - len(key) + 1)
      print("%s%s:%s%s" % ((" " * indent),key, seperate, dict[key]), end=endwith)
    if '\n' not in endwith:
      print('\n')

# Information Classes and Functions
def search(keyword):
  """Searches packages by keyword."""
  return json.loads(request.urlopen(SEARCH + keyword).read().decode())['results']

def info(package):
  """Returns information about a package."""
  return json.loads(request.urlopen(INFO + package).read().decode())['results']

def msearch(maintainer):
  """Searches for packages maintained by a certain maintainer."""
  return json.loads(request.urlopen(MSEARCH + maintainer).read().decode())['results'] 

def orphans():
  """Searches for orphaned packages."""
  return msearch('0');

def geturl(package, by='name'):
  """Gets the url of package by name or id."""
  if by == 'name':
    return CCR_PKG + "?ID=" + info(package)['ID']
  elif by == 'id':
    return CCR_PKG + "?ID=" + package

def getlatest(num=10):
  """Gets the info for the latest `num` CCR packages then returns as a list."""
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

# CCR Actions- Things done logged in!
class CCRSession(object):
  """The Class containing all the CCR actions."""

  def __init__(self, username, password):
    """Log in to the CCR and set a few variables."""
    # Allow username to be used across the class
    self.username = username
    # Initialize cookiejar and opener
    self.cj = cookiejar.CookieJar()
    self._opener = request.build_opener(request.HTTPCookieProcessor(self.cj))
    # Create login data string
    data = parse.urlencode({'user': username, 'passwd': password, 'remember_me': 'off'})
    # Log in. Ignore the 302 error.
    # If anyone knows how to fix this error please tell me.
    try:
      self._opener.open(CCR_BASE, data.encode())
    except error.HTTPError:
      pass
    except:
      print("Something weird happened.")
    # Test the login.
    checkstr = "packages.php?SeB=m&K=" + username
    currentHome = self._opener.open(CCR_BASE).read().decode()
    if not (checkstr in currentHome):
      print("Either your username or password is wrong or there was some other problem when logging in.")

  def __enter__(self):
    return self

  def close(self):
    """Close the session."""
    self._opener.close()

  def __exit__(self, type, value, traceback):
    """Deconstructor."""
    self.close()

  def flag(self, package):
    """Flags a package out of date."""
    ccrid = info(package)['ID']
    if info(package)['OutOfDate'] == "0":
      data = parse.urlencode({"IDs[%s]" % (ccrid): 1, "ID": ccrid, "do_Flag": 1}).encode()
      self._opener.open(CCR_PKG, data)
      if info(package)['OutOfDate'] == "0":
        print("Could not flag %s as out of date." % package)

  def unflag(self, package):
    """Unflags a package out of date."""
    ccrid = info(package)['ID']
    if info(package)['OutOfDate'] == "1":
      data = parse.urlencode({"IDs[%s]" % (ccrid): 1, "ID": ccrid, "do_UnFlag": 1}).encode()
      self._opener.open(CCR_PKG, data)
      if info(package)['OutOfDate'] == "1":
        print("Could not unflag %s as out of date." % package)

  def voted(self, package, by='name'):
    """Checks to see if user has voted for a package."""
    if by == 'name':
      ccrid = info(package)['ID']
    else:
      ccrid = package
    if "class='button' name='do_UnVote'" in self._opener.open(CCR_PKG + "?ID=" + ccrid).read().decode():
      return True
    else:
      return False

  def vote(self, package):
    """Votes for a package."""
    ccrid = info(package)['ID']
    # Check if the package has been voted for, if not vote for it
    if not self.voted(ccrid, by='id'):
      data = parse.urlencode({"IDs[%s]" % (ccrid): 1, "ID": ccrid, "do_Vote": 1}).encode()
      self._opener.open(CCR_PKG, data)
    # Check for success
    if not self.voted(ccrid, by='id'):
      print("Voting for %s failed." % package)

  def unvote(self, package):
    """Removes the user's vote for a package."""
    ccrid = info(package)['ID']
    # Check if the package has been voted for, if so remove the vote
    if self.voted(ccrid, by='id'):
      data = parse.urlencode({"IDs[%s]" % (ccrid): 1, "ID": ccrid, "do_UnVote": 1}).encode()
      self._opener.open(CCR_PKG, data)
    # Check for success
    if self.voted(ccrid, by='id'):
      print("Removing the vote for %s failed." % package)

  def delete(self, package):
    """Removes a package from the CCR."""
    ccrid = info(package)['ID']
    data = parse.urlencode({"IDs[%s]" % (ccrid): 1, "ID": ccrid, "do_Delete": 1, "confirm_Delete": 0}).encode()
    self._opener.open(CCR_PKG, data).read()
    # Test if package still exists
    if info(package) != 'No result found':
      print("Could not delete %s." % package)

  def notify(self, package):
    """Set notify for package."""
    ccrid = info(package)['ID']
    data = parse.urlencode({"IDs[%s]" % (ccrid): 1, "ID": ccrid, "do_Notify": 1}).encode()
    if "<option value='do_UnNotify'" not in self._opener.open(CCR_PKG, data).read().decode():
      print("Could not set notify for %s." % package)

  def unnotify(self, package):
    """Unset notify for package."""
    ccrid = info(package)['ID']
    data = parse.urlencode({"IDs[%s]" % (ccrid): 1, "ID": ccrid, "do_UnNotify": 1}).encode()
    if "<option value='do_Notify'" not in self._opener.open(CCR_PKG, data).read().decode():
      print("Could not unset notify for %s." % package)

  def adopt(self, package):
    """Adopt a package."""
    pkginfo = info(package)
    ccrid = pkginfo['ID']
    if pkginfo['Maintainer'] != '[PKGBUILD error: non-UTF8 character]':
      print("Attempting to adopt maintained package.")
    data = parse.urlencode({"IDs[%s]" % (ccrid): 1, "ID": ccrid, "do_Adopt": 1}).encode()
    self._opener.open(CCR_PKG, data).read()
    pkginfo = info(package)
    if pkginfo['Maintainer'] != self.username:
      print("Could not adopt %s." % package)

  def disown(self, package):
    """Disown a package."""
    pkginfo = info(package)
    ccrid = pkginfo['ID']
    data = parse.urlencode({"IDs[%s]" % (ccrid): 1, "ID": ccrid, "do_Disown": 1}).encode()
    self._opener.open(CCR_PKG, data).read()
    pkginfo = info(package)
    if pkginfo['Maintainer'] == self.username:
      print("Could not disown %s." % package)

#  def submit(self, f, category):
#    """Sumbit a package to CCR."""
#    error = re.compile(r"<span class='error'>(?P<message>.*)</span>")
#    params = {"pkgsubmit": 1, "category": CATEGORY_NUMS[category], "pfile": open(f, "rb")}

  def setcategory(self, package, category):
    """Change the category of a package in the CCR."""
    pkginfo = info(package)
    ccrid = pkginfo['ID']
    try:
      data = parse.urlencode({"action": "do_ChangeCategory", "category_id": CATEGORY_NUMS[category]}).encode()
    except KeyError:
      print("%s is an invalid category." % category)
    pkgurl = CCR_PKG + "?ID=" + ccrid
    response = self._opener.open(pkgurl, data).read().decode()
    checkstr = "selected='selected'>" + category + "</option>"
    if checkstr not in response:
      print("Something seems to have gone wrong when changing the category.")

# Redis DB Stuff
class RedisCCR(object):
  def __init__(self):
    self.r = redis.StrictRedis(db=3)

  def needsUpdate(self):
    """Test whether updatePackages should be executed."""
    return True if self.r.keys("ccr:packages:*") == [] else False

  def updatePackages(self):
    """Update the Redis Database with the newest Package information."""
    todel = self.r.keys("ccr:packages:*")
#    todel += self.r.keys("ccr:ids:*")
    if todel != []:
      for val in todel:
        self.r.delete(val)
    pipe = self.r.pipeline()
    newdata = getlatest(getlatest(1)[0]['ID'])
    for package in newdata:
      for key in package.keys():
        if key != 'Name':
          storeHash = 'ccr:packages:' + package['Name']
          pipe.hset(storeHash, key, package[key])
          pipe.expire(storeHash, EXPIRE)
#      storeHash = 'ccr:ids:' + package['ID']
#      pipe.set(storeHash, package['Name'])
#      pipe.expire(storeHash, EXPIRE)
    pipe.execute()

# Test
if __name__ == "__main__":
  printDict(info("ffpy"))
