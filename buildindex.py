import re
import math

import nltk
from sklearn.feature_extraction.text import TfidfVectorizer

class Build_Index(object):

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
        
        self.file_to_terms = self.process_files(fnames)
        self.regdex = self.make_indices(self.file_to_terms)
        self.inverted_index = self.invert_index(self.regdex)
        self.dict_doc_vectors = self.create_document_vectors()
        
    def process_files(self, fnames):
        """Given list of fnames, return dict of {fnames: [words].
        
        returns
        -------
        file_to_terms : dict
            key = fname, values = list of word tokens
        """
        file_to_terms = {}
        for file in fnames:
            f = open(file, 'r')
            line = f.read()[:100]
            text = line.lower()
            file_to_terms[file] = nltk.word_tokenize(text)
            f.close()
        return file_to_terms
    

    def make_indices(self, file_to_terms):
        """
        parameters
        ----------
        file_to_terms : dict where k = fname, v = [tokens]

        returns
        -------
        total : dict where k = fname, v = {token1:[pos1, pos3], token2: [pos2]}
        """
        total = {}
        for doc_id in file_to_terms.keys():
            total[doc_id] = self._index_one_file(file_to_terms[doc_id])
        return total
    
    
    def _index_one_file(self, list_tokens):
        """
        parameters
        ----------
        list_tokens : list

        returns
        -------
        word_pos : dict
            k = words, v = position

        example
        -------
        >>> tokens = ['this', 'is', 'vin']
        >>> index_one_file(tokens)
        {'is': [1], 'this': [0], 'vin': [2]}
        """
        word_pos = {}
        for i, word in enumerate(list_tokens):
            if word in word_pos.keys():
                word_pos[word].append(i)
            else:
                word_pos[word] = [i]
        return word_pos

    def invert_index(self, regdex):
        """
        parameters
        ----------
        {fname: {token: [pos1, pos2, ...], ... }}

        returns
        -------
        {token: {fname: [pos1, pos2]}, ...}, ...}
        """
        total_index = {}
        for fname in regdex.keys():
            for token in regdex[fname].keys():
                if token in total_index.keys():
                    if fname in total_index[token].keys():
                        total_index[token][fname].append(regdex[fname][token][:])
                    else:
                        total_index[token][fname] = regdex[fname][token]
                else:
                    total_index[token] = {fname: regdex[fname][token]}
        return total_index

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