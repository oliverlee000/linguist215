'''
clean_dataset.py

Generic script to get rid of any nonalphanumeric character in the dataset
'''
import re, pandas as pd, os

def main():
    fn = 'chunk_df_comma_split.csv'
    col = 'chunk'
    df = pd.read_csv(fn)
    cleaned_column = [re.sub(r'[`’]', '\'', r) for r in df[col]]
    df[col] = cleaned_column
    filebasename = os.path.splitext(fn)[0]
    df.to_csv(filebasename + '_cleaned.csv')
    

if __name__ == '__main__':
    main()