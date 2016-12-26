
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
      print("Something bad happened")
      return

  keepRecord = file_list.pop(index)
  print("Keeping: %s" % keepRecord)
  for delfile in file_list:
    print("Deletting: %s" % delfile)
