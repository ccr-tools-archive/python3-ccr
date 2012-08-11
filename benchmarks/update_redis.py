import ccrlib
import cProfile

rccr = ccrlib.RedisCCR()

cProfile.run('rccr.updatePackages()')
