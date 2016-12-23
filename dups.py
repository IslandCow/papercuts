#!/usr/bin/python3
import argparse
import io
import os
import os.path
import sqlite3
import sys
from db import db

def printDups(conn, limit):
    res = db.fetchExactDuplicates(conn, limit)
    coll = list()
    for fname in res:
        records = db.fetchFilesByFileName(conn, fname)
        coll.append(records)
    return coll

parser = argparse.ArgumentParser(description='Remove duplicate records.')
parser.add_argument('--scan', action='store_true', help='print duplicate records')
parser.add_argument('--delete', action='store_true', help='remove duplicate records')
parser.add_argument('--dups', action='store_true', help='list files with duplicate hashes')
args = parser.parse_args()

conn = sqlite3.connect('index.db')

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
    coll = printDups(conn, 2000)
    for records in coll:
        records.pop(0)
        keys = [r.key for r in records]
        print('Duplicates to be deleted: %s' % keys)
        res = db.deleteFiles(conn, keys)
        print(res)
    print(db.countFiles(conn))
    conn.commit()
    sys.exit(0)

if args.dups:
    dups = db.findDuplicateHashes(conn, 10, 10000)
    for dup in dups:
        f_dups = db.fetchFilesByHash(conn, dup)
        print(dup)
        print([f.abs_path for f in f_dups])

print("DONE")
