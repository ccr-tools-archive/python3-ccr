import ccrlib
import cProfile

rccr = ccrlib.RedisCCR()
def main():
  # Check for expiration, causes slowness
  if rccr.needsUpdate():
    rccr.updatePackages()
  # Search, doesn't include description like remoteSearch does. May add later.
  print("\n\n\nSearch!\n\n\n")
  rccr.search('python3-')

  print("\n\n\nInfo!\n\n\n")
  rccr.info('python3-redis-git')

  print("\n\n\nMSearch!\n\n\n")
  rccr.msearch('stephenmac7')

  print("\n\n\nOrphans!\n\n\n")
  rccr.orphans()

  print("\n\n\nGetURL!\n\n\n")
  rccr.geturl('python3-redis-git')

cProfile.run('main()')
