import argparse
import io
import os
import os.path
import sqlite3
import sys
from db import db

def processFile(path):
    if os.path.isdir(path):
        # do not process directories
        return

    stats = db.readFile(path)
    f = os.path.split(path)
    parent_dir = os.path.split(f[0])[1]
    split_name = os.path.splitext(f[1])
    f_name = split_name[0]
    ext = split_name[1]

    print(stats)

    db.createFile(conn, path, parent_dir, f_name, ext, *stats)

def walk(path):
    for root, dirs, files in os.walk(path):
        for f in files:
            processFile(os.path.join(root, f))

        msg = 'Processed files in {}'.format(root)
        print(msg)
        for d in dirs:
            walk(os.path.join(root, d))

        msg = 'Finished processing directories for {}'.format(root)
        print(msg)

parser = argparse.ArgumentParser(description='Index a folder of files.')
parser.add_argument('--new_db', action='store_true', help='if provided, the database file will be created')
parser.add_argument('--root', action='store', required=True, help='provide the root path')
args = parser.parse_args()

conn = sqlite3.connect('index.db')

if args.new_db:
    db.createTable(conn)
    print("tables created")

path = args.root

is_dir = os.path.isdir(path)
if not is_dir:
    print("A directory must be provided")
    sys.exit(1)

walk(os.path.abspath(path))

conn.close()
print("DONE")
