import os

def shortestString(file_list):
  shortest = None
  dups = False
  for f in file_list:
    if shortest == None:
      shortest = f
      continue
    
    if len(shortest) > len(f):
      shortest = f
      dups = False
    elif len(shortest) == len(f):
      dups = True

  return dups, file_list.index(shortest), shortest

def keepShortest(file_list):
  keepRecord = None
  deleteRecords = list()
  dups, index, shortest = shortestString([f.file_name for f in file_list])
  if dups:
    dups, index, shortest = shortestString([f.abs_path for f in file_list])
    if dups:
      print("Making arbitrary decision.")
      dups = False
      index = 0
      shortest = file_list[0] 

  keepRecord = file_list.pop(index)
  print("Keeping: %s" % keepRecord)
  if not os.path.exists(keepRecord.abs_path):
    print("Keep file not found, bail")

  for delfile in file_list:
    print("Deletting: %s" % delfile)
    path = delfile.abs_path
    if not os.path.exists(path):
      print("Skip missing path: %s" % path)
      continue
    os.remove(delfile.abs_path)    
