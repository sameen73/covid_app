import sqlite3
import pandas as pd

conn = sqlite3.connect('covid_tables.db')

print("This works I guess?")

df = pd.read_csv(r"C:\Users\USER\Documents\Misc\covid19_research\abstract_cleaned.csv")
df.to_sql('search_engine_table', conn)

df = pd.read_csv(r"C:\Users\USER\Documents\Misc\covid19_research\conclusion.csv")
df.to_sql('random_insights_table', conn)
print("Data Frame successfully read in")



