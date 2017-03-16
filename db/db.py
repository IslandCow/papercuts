import hashlib
import os
import sqlite3

class FileRecord:
    def __init__(self, key, abs_path, md5, parent, file_name, extension, size, date_created, date_modified):
        self.key = key
        self.abs_path = abs_path
        self.md5 = md5
        self.parent = parent
        self.file_name = file_name
        self.extension = extension
        self.size = size
        self.date_created = date_created
        self.date_modified = date_modified
    
    def __str__(self):
       joiner = "|"
       return joiner.join((str(self.key), self.file_name, self.abs_path))

def fileFromResult(result):
    return FileRecord(result['id'], result['absolute_path'], result['md5_sum'], result['parent_dir'], result['file_name'], 
            result['extension'], result['file_size'], result['date_created'], result['date_modified'])

def countFiles(conn):
    c = conn.cursor()
    c.execute('''SELECT COUNT(id) FROM file''')
    return c.fetchone()

def allFileNames(conn):
    c = conn.cursor()
    c.execute('''SELECT id, absolute_path FROM file''')
    return c.fetchall()

def fetchFileById(conn, key):
    c = conn.cursor()
    c.execute('''SELECT id, absolute_path, md5_sum, parent_dir, file_name, extension, file_size, date_created, date_modified FROM file WHERE id=?''', (key,))
    result = c.fetchone()
    return fileFromResult(result)

def deleteFiles(conn, keyList):
    c = conn.cursor()
    c.executemany("""DELETE FROM file WHERE id=?""", [(k,) for k in keyList])
    return c.fetchone()

def fetchFilesByHash(conn, f_hash):
    c = conn.cursor()
    c.execute('''SELECT id, absolute_path, md5_sum, parent_dir, file_name, extension, file_size, date_created, date_modified FROM file WHERE md5_sum=?''', (f_hash,))
    results = list()
    for res in c.fetchall():
        converted = FileRecord(*res)
        results.append(converted)
    return results

def fetchFilesByFileName(conn, file_name):
    c = conn.cursor()
    c.execute('''SELECT id, absolute_path, md5_sum, parent_dir, file_name, extension, file_size, date_created, date_modified FROM file WHERE absolute_path=?''', (file_name,))
    results = list()
    for res in c.fetchall():
        converted = FileRecord(*res)
        results.append(converted)
    return results

def findDuplicateHashes(conn, size, limit):
    c = conn.cursor()
    c.execute('''SELECT md5_sum FROM file WHERE file_size > ? GROUP BY md5_sum HAVING COUNT(id) > 1 LIMIT ?''', (size, limit))
    results = list()
    for res in c.fetchall():
      results.append(res[0])
    return results

def fetchExactDuplicates(conn, limit):
    c = conn.cursor()
    c.execute('''SELECT absolute_path FROM file GROUP BY absolute_path HAVING COUNT(id) > 1 LIMIT ?''', (limit,))
    results = list()
    for res in c.fetchall():
      results.append(res[0])
    return results

def createTable(conn):
	print("Creating file table")
	c = conn.cursor()
	c.execute('''CREATE TABLE file (id integer primary key, absolute_path text, md5_sum text, parent_dir text, file_name text, extension text, file_size integer, date_created integer, date_modified integer)''')
	conn.commit()

def checkForFile(conn, file_name):
	files = fetchFilesByFileName(conn, file_name)
	print('Instances of file %s (%d)' % (file_name, len(files)))
	return len(files) > 0


def createFile(conn, path, p_dir, file_name, extension, md5, size, created, modified):
	print("insert file %s" % (path))
	c = conn.cursor()
	query_template = '''INSERT INTO file (file_name, parent_dir, extension, absolute_path, md5_sum, file_size, date_created, date_modified) VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''
	c.execute(query_template, (file_name, p_dir, extension, path, md5, size, created, modified))
	conn.commit()

def hashFile(binary_data):
	hasher = hashlib.md5()
	hasher.update(binary_data)
	return hasher.hexdigest()

def readFile(relative_path):
	file_stat = os.stat(relative_path)
	f = open(relative_path, 'rb')	
	file_data = f.read()
	md5 = hashFile(file_data)
	return (md5, file_stat.st_size, file_stat.st_ctime_ns, file_stat.st_mtime_ns)

