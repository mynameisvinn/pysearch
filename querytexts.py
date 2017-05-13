from buildindex import Build_Index
import re

#NEED TO TEST MORE.

#input = [file1, file2, ...]
#res = {word: {filename: {pos1, pos2}, ...}, ...}
class Query:

	def __init__(self, fnames):
		self.index = Build_Index(fnames)  # instantiate an index called index
		self.inverted_index = self.index.inverted_index  # grab its inverted index
		self.regularIndex = self.index.regdex


	def one_word_query(self, word):
		if word in self.inverted_index.keys():
			return [docID for docID in self.inverted_index[word].keys()]
		else:
			return []