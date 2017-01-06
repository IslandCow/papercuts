#!/usr/bin/python3
import argparse
import io
import os
import os.path
import sqlite3
import sys
from db import db
from file import file

def printDups(conn, limit):
    res = db.fetchExactDuplicates(conn, limit)
    coll = list()
    for fname in res:
        records = db.fetchFilesByFileName(conn, fname)
        coll.append(records)
    return coll

def deleteDups(conn):
    coll = printDups(conn, 20)
    for records in coll:
        records.pop(0)
        keys = [r.key for r in records]
        print('Duplicates to be deleted: %s' % keys)
        res = db.deleteFiles(conn, keys)
        print(res)
    print(db.countFiles(conn))
    return len(coll)

parser = argparse.ArgumentParser(description='Remove duplicate records.')
parser.add_argument('--scan', action='store_true', help='print duplicate records')
parser.add_argument('--delete', action='store_true', help='remove duplicate records')
parser.add_argument('--dups', action='store_true', help='list files with duplicate hashes')
parser.add_argument('--clean_dups', action='store_true', help='removes duplicate files.  Keeps the file with the shortesst name')
parser.add_argument('--clean', action='store_true')
args = parser.parse_args()

print("WELCOME TO DUPS")
conn = sqlite3.connect('index.db')
print("SQLITE DB LOADED")

if args.scan:
    coll = printDups(conn, 1000)
    total = 0
    for records in coll:
        count = len(records)
        total = total + count
        print(count)
        print(records)
    print("Dups: %d" % total)
    conn.commit()
    sys.exit(0)

if args.delete:
    for i in range(0,10000000):
        print("Start iteration %d" % i)
        changes = deleteDups(conn)
        if changes == 0:
            print("Out of dups!")
            break
        if i % 5 == 0:
            conn.commit()
    conn.commit()
    sys.exit(0)

if args.clean:
    all_files = db.allFileNames(conn)
    deleted_files = list()
    for f in all_files:
      if not os.path.exists(f[1]):
        print("Remove record %s" % f[0])
        deleted_files.append(f[0])
    db.deleteFiles(conn, deleted_files)
    conn.commit()
    sys.exit(0)

if args.clean_dups:
    dups = db.findDuplicateHashes(conn, 10, 10000)
    for dup in dups:
        f_dups = db.fetchFilesByHash(conn, dup)
        file.keepShortest(f_dups)
    print("WOO")
    sys.exit(0)

if args.dups:
    dups = db.findDuplicateHashes(conn, 10, 10000)
    for dup in dups:
        f_dups = db.fetchFilesByHash(conn, dup)
        print(dup)
        print([f.abs_path for f in f_dups])

print("DONE")
