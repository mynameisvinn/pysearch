import nltk

def doc2tokens(fnames, cutoff=1000):
    """
    parameters
    ----------
    fnames : list of fnames
    cutoff : int
        number of characters to read from file
    
    returns
    -------
    dict where key = fname, value = list of tokens
    """
    file_to_terms = {}
    for file in fnames:
        f = open(file, 'r')
        line = f.read()[:cutoff]
        text = line.lower()
        file_to_terms[file] = nltk.word_tokenize(text)
        f.close()
    return file_to_terms


def invert_index(regdex):
    """
    takes a kv where k=fname, v=[token1, token2,...] and
    inverts it such that k=token1, v=[fname1, fname2,...]
    """
    inverted_index = {}

    # for each document...
    for fname in regdex.keys():

        # ...inspect its tokens
        for token in regdex[fname]:

            # if token exists, append fname
            if token in inverted_index.keys():
                if fname in inverted_index[token]:
                    pass
                else:
                    inverted_index[token].append(fname)
                    
            # otherwise create a new entry
            else:
                inverted_index[token] = [fname]
    return inverted_index