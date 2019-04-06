import pandas as pd

#Test loading data back
pd.read_csv('df_joined.csv', index_col=False).head()


#with open('/data/dict_category.json', 'r') as f:
 #   print(json.load(f))