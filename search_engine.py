#Load libraries (within function to try and avoid circular imports)
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
#import sklearn.feature_extraction.text as thing
from sklearn.metrics.pairwise import cosine_similarity
#import sklearn.metrics.pairwise as other_thing

def covid_search(data, query, n_results = 50):
    
    #Insert filtration of abstracts without query words here
    query_as_set = set(query)
    
    #Filtering for rows that contain at least one of the query tokens
    data_sub = data.loc[data.abstract2.apply(lambda x: len(query_as_set.intersection(x)) >= 1)]
    data_sub.reset_index(inplace = True, drop = True)
    
    #Rejoin 
    clean_query = ' '.join(query)
    
    #Figure out this statement later, refers to subset of data outside of function
    abstracts = data_sub.abstract2.tolist()
    abstracts = [' '.join(list_val) for list_val in abstracts] #= ' '.join(abstracts)#.apply(lambda x:' '.join(x))

    #Add query to list object (n+1 total documents)
    abstracts.append(clean_query)

    #Create TF-IDF vectorizer object 
    tv = TfidfVectorizer(norm = 'l2', use_idf = True, smooth_idf= True, lowercase=False,\
                         analyzer="word", token_pattern=r"(?u)\S\S+")

    #Run TF-IDF fit transform and convert to array on all documents + query
    tv_matrix = tv.fit_transform(abstracts)
    tv_matrix = tv_matrix.toarray()

    if tv_matrix.shape[0] == 1:
        column_names = ["cord_uid", "title", "abstract"]

        final_results = pd.DataFrame(columns = column_names) 
    
    else:
        #if tv_matrix.
        #Calculate cosine similarity between each of n documents and the query (last entry of list)
        cos_sim_matrix = cosine_similarity(tv_matrix[:-1,],tv_matrix[-1,].reshape(1,-1))
        
        #Compiling results into dataframe 
        results = pd.DataFrame(cos_sim_matrix)
        #print("Results created:"+ str(results.shape))
        #Sort based on cosine similarity column (labeled 0 by default)
        results = results.sort_values(0, ascending = False)

        #Merge in original abstract column
        results = results.merge(data_sub.abstract,left_index=True, right_index=True, how='left')

        #Merge in cord_uid column 
        results = results.merge(data_sub.cord_uid,left_index=True, right_index=True, how= 'left')

        #Merge in title column
        results = results.merge(data_sub.title,left_index=True, right_index=True, how= 'left')

        #Renaming columns for better readability
        results.rename(columns={0:"cosine_similarity"}, inplace=True)

        if results.shape[0] >= n_results:
            results_ = results.iloc[0:n_results,]
            final_results = results_[['cord_uid', 'title', 'abstract']]
        else:
            final_results = results[['cord_uid', 'title', 'abstract']]

    return final_results