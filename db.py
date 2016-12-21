import hashlib

def createTable(conn):
	print("Creating file table")
	c = conn.cursor()
	c.execute('''CREATE TABLE file (id integer primary key, absolute_path text, md5_sum text, parent_dir text, file_name text, extension text, file_size integer, date_created integer, date_modified integer)''')
	conn.commit()

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

