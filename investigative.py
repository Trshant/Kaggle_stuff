import pandas as pd
import numpy as np

file_under_investigation = "./datasets/homicide_database.csv"
investigate_df = pd.read_csv(file_under_investigation ,  sep=',', error_bad_lines=False, index_col=False, dtype='unicode'  )

columns =  investigate_df.columns.tolist()

'''
this bit of code shows the column header and all the values.
''' 
for column in columns :
	print column
	print ''
	print investigate_df[column].unique()
	print ''



## this bit is entirely for my own learning/pleasure
