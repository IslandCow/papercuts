import argparse
import io
import os
import os.path
import sqlite3
import sys
import indexer.db as db

parser = argparse.ArgumentParser(description='Index a folder of files.')
parser.add_argument('-a', action='store_true')

args = sys.argv
if len(args) != 2:
  print("missing file name")
  sys.exit(1)

conn = sqlite3.connect('index.db')

if sys.argv[1] == '-a':
	db.createTable(conn)
	print("tables created")
	sys.exit(0)

path = os.path.abspath(sys.argv[1])

is_dir = os.path.isdir(path)
if is_dir:
	print("Directories not currently supported")
	sys.exit(1)

stats = readFile(path)
f = os.path.split(path)
parent_dir = os.path.split(f[0])[1]
split_name = os.path.splitext(f[1])
f_name = split_name[0]
ext = split_name[1]

print(stats)

db.createFile(conn, path, parent_dir, f_name, ext, *stats)

conn.close()
print("DONE")
