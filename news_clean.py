import os
import shutil
filelist=[]
dir1="./Result/"
dir2="./News/"
for dir in [dir1, dir2]:
  filelist=os.listdir(dir)
  for f in filelist:
    filepath = os.path.join( dir, f )
    if os.path.isfile(filepath):
      os.remove(filepath)
      print filepath+" removed!"
    elif os.path.isdir(filepath):
      shutil.rmtree(filepath,True)
      os.makedirs(filepath+'/')
      print filepath + " cleaned!"
