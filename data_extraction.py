import sqlite3
from pandas import DataFrame

def connect_n_select(db_file):
    
    #Connecting to the database file
    conn = sqlite3.connect(db_file)

    #Creating a cursor object
    cur = conn.cursor()

    #Calling in all rows and the 4 required columns from the search engine table in the database
    cur.execute("SELECT cord_uid, title, abstract, abstract2 FROM search_engine_table")

    #Creating a dataframe via fetchall()
    df = DataFrame(cur.fetchall())

    #Getting a list of column names from the cur object
    col_name_list = [tuple[0] for tuple in cur.description]

    #Changing column names to col_name_list
    df.columns = col_name_list
    
    df.abstract2 = df['abstract2'].apply(eval)

    #df.abstract2 = df['abstract2'].apply(lambda x: ' '.join(x))
    
    #Add code to pull from random insight generator table once you get the first one working.
    #cur.execute("SELECT ")
    #else if table == 2: 
    #    cur.execute("SELECT")
    conn.close()
    #print(df.shape)
    return df

def conclusion_pick(db_file):

    #Connecting to sqlite database file
    conn = sqlite3.connect(db_file)

    #Creating a cursor object
    cur = conn.cursor()

    #Calling in all rows and the 3 required columns from the conclusions table in the database
    cur.execute("SELECT cord_uid, title, conclusion FROM random_insights_table\
                 ORDER BY RANDOM() LIMIT 10")

    #Creating a dataframe via fetchall()
    df = DataFrame(cur.fetchall())

    #Getting a list of column names from the cur object
    col_name_list = [tuple[0] for tuple in cur.description]

    #Changing column names to col_name_list
    df.columns = col_name_list

    #Close connection to database
    conn.close()

    return df
