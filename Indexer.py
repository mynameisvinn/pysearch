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