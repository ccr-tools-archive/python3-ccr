import ccrlib
import cProfile

rccr = ccrlib.RedisCCR()
# Check for expiration, causes slowness
if rccr.needsUpdate():
  rccr.updatePackages()
# Search, doesn't include description like remoteSearch does. May add later.
print("Search!")
cProfile.run("rccr.search('python3-')")

print("Info!")
cProfile.run("rccr.info('python3-redis-git')")

print("MSearch!")
cProfile.run("rccr.msearch('stephenmac7')")

print("Orphans!")
cProfile.run("rccr.orphans()")

print("GetURL!")
cProfile.run("rccr.geturl('python3-redis-git')")
