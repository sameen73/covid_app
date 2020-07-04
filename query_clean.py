from nltk import word_tokenize, WordNetLemmatizer

def query_cleaner(text_input):
    query = text_input
    #Tokenize query into words
    query = word_tokenize(query)
    
    #Lowercase query the same way the data was lowercased
    lower_case_query = []
    for term in query:
        if len(term) > 2 and sum(1 for c in term if c.isupper()) <= 1:
            lower_case_query.append(term.lower())
        else:
            lower_case_query.append(term)

    #Lemmatize query
    lemmatizer = WordNetLemmatizer()
    clean_query = []
    for term in lower_case_query:
        clean_query.append(lemmatizer.lemmatize(term))

    return clean_query