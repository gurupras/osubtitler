import os
import hashlib, zlib, base64, struct

from pycommons.file_entry import FileEntry

class File(FileEntry):
	DEF_BLOCK_SIZE = 2 * 1024 * 1024 #2MB

	def checksum(self, algorithm_name, blocksize=DEF_BLOCK_SIZE):
		try:
			alg_obj = getattr(hashlib, algorithm_name)
		except Exception as e:
			print 'Could not find algorithm \'%s\'' % (algorithm_name)
			raise e
		alg = alg_obj()

		assert os.path.isfile(self.path()), 'Attempting to call checksum() on something that is not a file'
		with open(self.path(), 'rb') as f:
			while True:
				buf = f.read(blocksize)
				if not buf:
					break
				alg.update(buf)
		return alg.hexdigest()

	'''
	hashfile algorithm as implemented on
	http://trac.opensubtitles.org/projects/opensubtitles/wiki/HashSourceCodes
	'''
	def hash_file(self):
		longlongformat = '<q'  # little-endian long long
		bytesize = struct.calcsize(longlongformat)

		file_hash = None
		with open(self.path(), "rb") as f:
			filesize = os.path.getsize(self.path())
			file_hash = filesize

			if filesize < 65536 * 2:
			   raise Exception("SizeError")

			for x in range(65536 / bytesize):
				buf = f.read(bytesize)
				(l_value,)= struct.unpack(longlongformat, buf)
				file_hash += l_value
				file_hash = file_hash & 0xFFFFFFFFFFFFFFFF #to remain as 64bit number


			f.seek(max(0, filesize - 65536), 0)
			for x in range(65536 / bytesize):
				buf = f.read(bytesize)
				(l_value,)= struct.unpack(longlongformat, buf)
				file_hash += l_value
				file_hash = file_hash & 0xFFFFFFFFFFFFFFFF

			returnedhash =  "%016x" % file_hash
		return returnedhash

