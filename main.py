import argparse
import io
import os
import os.path
import sqlite3
import sys
from db import db

parser = argparse.ArgumentParser(description='Index a folder of files.')
parser.add_argument('-a', action='store_true', help='if provided, the database file will be created')
parser.add_argument('--root', action='store', required=True, help='provide the root path')
args = parser.parse_args()

path = args.root

conn = sqlite3.connect('index.db')

is_dir = os.path.isdir(path)
if is_dir:
	print("Directories not currently supported")
	sys.exit(1)

stats = db.readFile(path)
f = os.path.split(path)
parent_dir = os.path.split(f[0])[1]
split_name = os.path.splitext(f[1])
f_name = split_name[0]
ext = split_name[1]

print(stats)

db.createFile(conn, path, parent_dir, f_name, ext, *stats)

conn.close()
print("DONE")
