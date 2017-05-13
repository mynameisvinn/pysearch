import re
import math
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer

class Build_Index:

	def __init__(self, fnames):
		"""
		Parameters
		----------
		fnames : list
			List of fpaths to documents. Example is [file1, file2, ...]

		Returns
		-------
		inverted_index : dict of dict of lists
			{word: {fname: [pos1, pos2]}, ...}, ...}
		"""
		
		self.file_to_terms = self.process_files(fnames)  # returns {docID : [word1, word2, ...]}
		self.regdex = self.make_indices(self.file_to_terms)  # returns {docID: {word: [pos1, pos2, ...]}, ...}
		self.inverted_index = self.invert_index()  # returns {word: {fname: [pos1, pos2]}, ...}, ...}
		self.dict_doc_vectors = self.create_document_vectors()


	def create_document_vectors(self):
		"""Create td-idf for documents.
		
		Returns
		-------
		dict_doc_vectors : {doc1:[vector], doc2:[vector], ... }
		"""
		corpus = self._create_corpus(self.file_to_terms)
		tf_matrix = TfidfVectorizer(stop_words = 'english').fit_transform(corpus).todense().tolist()
		
		dict_doc_vectors = {}
		for i, k in enumerate(self.file_to_terms):
			dict_doc_vectors[k] = tf_matrix[i]
		return dict_doc_vectors


	def _create_corpus(self, dict_of_ls_tokens):
		"""Create corpus to fit vectorizer
		
		Parameter
		---------
		dict_of_ls_tokens : {docID : [word1, word2, ...]}

		Returns
		-------
		corpus : list of strings. eg [string1, string2, ...]
		"""
		corpus = []
		for ls_tokens in dict_of_ls_tokens.values():
			corpus.append(' '.join(ls_tokens))
		return corpus


	def process_files(self, fnames):
		"""Given list of filenames, generate dict.

		Parameters
		----------
		fnames : list of str
			Example is [fname1, fname2, ...]

		Returns
		-------
		file_to_terms : dict of lists
			Keys refer to document ID. Values represent list of tokens. Example: {docID : [word1, word2, ...]}
		"""

		file_to_terms = {}
		for file in fnames:
			f = open(file, 'r')
			for line in f.xreadlines():
				text = line.decode('utf-8').lower()
				file_to_terms[file] = nltk.word_tokenize(text)
			f.close()
		return file_to_terms

	
	def _index_one_file(self, list_tokens):
		"""
		Parameters
		----------
		list_tokens : list
			List of tokens in document: [word1, word2, ...]

		Returns
		-------
		fileIndex : dict
			Dict of unique words and their locations in the document: {word1: [pos1, pos2], word2: [pos2, pos434], ...}

		Example
		-------
		>>> tokens = ['this', 'is', 'vin']
		>>> index_one_file(tokens)
		{'is': [1], 'this': [0], 'vin': [2]}
		"""
		word_positions = {}
		for i, word in enumerate(list_tokens):
			if word in word_positions.keys():
				word_positions[word].append(i)
			else:
				word_positions[word] = [i]
		return word_positions

	
	def make_indices(self, termlists):
		"""
		Parameters
		----------
		termlists : dict. 
  			Keys refer to document ID. Values represent list of tokens. Example: {docID: [word1, word2, ...], ...}

		Returns
		-------
		total : dict
    		Keys refer to document ID. Values contain dict of word locations. Example: {docID: {word: [pos1, pos2, ...]}, ...}
		"""
		total = {}
		for doc_id in termlists.keys():
			total[doc_id] = self._index_one_file(termlists[doc_id])
		return total


	def invert_index(self):
		"""Inversion.

		Parameters
		----------
		{filename: {word: [pos1, pos2, ...], ... }}  # created by make_indices()

		Returns
		-------
		{word: {filename: [pos1, pos2]}, ...}, ...}
		"""
		total_index = {}
		indie_indices = self.regdex  # fetches {docID: {word: [pos1, pos2, ...]}, ...}
		for filename in indie_indices.keys():
			for word in indie_indices[filename].keys():
				if word in total_index.keys():
					if filename in total_index[word].keys():
						total_index[word][filename].append(indie_indices[filename][word][:])
					else:
						total_index[word][filename] = indie_indices[filename][word]
				else:
					total_index[word] = {filename: indie_indices[filename][word]}
		return total_index