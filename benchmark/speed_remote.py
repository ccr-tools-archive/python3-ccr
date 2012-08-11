import ccrlib
import cProfile

def main():
  print("\n\n\nSearch!\n\n\n")
  print(ccrlib.searchRemote('python3-'))

  print("\n\n\nInfo!\n\n\n")
  print(ccrlib.infoRemote('python3-redis-git'))

  print("\n\n\nMSearch!\n\n\n")
  print(ccrlib.msearchRemote('stephenmac7'))

  print("\n\n\nOrphans!\n\n\n")
  print(ccrlib.orphansRemote())

  print("\n\n\nGetURL!\n\n\n")
  print(ccrlib.geturlRemote('python3-redis-git'))

cProfile.run('main()')
