import ccrlib
import cProfile

print("Search!")
cProfile.run("ccrlib.searchRemote('python3-')")

print("Info!")
cProfile.run("ccrlib.infoRemote('python3-redis-git')")

print("MSearch!")
cProfile.run("ccrlib.msearchRemote('stephenmac7')")

print("Orphans!")
cProfile.run("ccrlib.orphansRemote()")

print("GetURL!")
cProfile.run("ccrlib.geturlRemote('python3-redis-git')")
