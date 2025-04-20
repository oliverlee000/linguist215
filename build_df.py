import os, re, pandas as pd
'''
main.py
April 7, 2025
A series of helper functions for processing the fairy tale data.
'''



'''
Given str text representing an html site, first extract each of the
paragraphs in the html. Then, for each paragraph, split into chunks of words
immediately preceding a punctuation mark. 

text - html of a given website
source_file - name of the html
split_by_comma - TRUE if text should be split by commas

Assumes:
df columns are ['chunk', 'punctuation_mark', 'word_count', 'source_file']

Returns:
chunk_df - dataframe containing chunks of words immediately preceding a
punctuation mark

'''
def chunk(text, source_file, split_by_comma=True):
    chunk_df = pd.DataFrame(columns=['chunk', 'punctuation_mark', 'word_count', 'source_file'])
    # 0. Reformat html to take out newlines (except at ends of paragraphs) and convert HTML encodings to unicode
    text = re.sub('[ \n]+', ' ', text)
    text = re.sub('</[pP]>', '</p>\n', text)
    text = re.sub('&mdash;', '—', text)
    text = re.sub('&ndash;', '–', text)
    text = re.sub('&rsquo;|&lsquo;', '\'', text) # Convert to Unicode single quotation marks
    text = re.sub('&rdquo;|&ldquo;', '\"', text) # Convert to Unicode double quotation marks 
    text = re.sub('<a.*>.*</a>', '', text) # Take out all <a> ... </a> strings
    # 1. Extract each paragraph in the html
    paragraph_pattern = '(?<=<[pP]>).*(?=</[pP]>)'
    paragraphs = re.findall(paragraph_pattern, text)
    # 2. Break into chunks
    for paragraph in paragraphs:
        chunk_pattern = r'(\w[^,\.\?!:;—–]*)([,\.\?!:;—–] ?)' if split_by_comma else r'(\w[^\.\?!:;—–]*)([\.\?!:;—–] ?)'
        chunk_iter = re.finditer(chunk_pattern, paragraph)
        for match in chunk_iter:
            chunk, punct_mark = match.group(1), match.group(2)
            word_count = len(re.split(r' ', chunk))
            chunk_df.loc[len(chunk_df)] = [chunk, punct_mark, word_count, source_file]
    return chunk_df

'''
Iterate through each html files in data, feed
into pantameterize().
'''
def main():
    folder_path = 'data'
    os.chdir(folder_path)
    htmls = [] # List of tuples contianing path name and html text bodies
    for file in os.listdir():
        if file.endswith('.html'):
            file_path = os.path.join(os.getcwd(), file)
            f = open(file_path, 'r')
            htmls.append((f.read(), folder_path + '/' + file))
    os.chdir('..')
    df_columns = ['chunk', 'punctuation_mark', 'word_count', 'source_file']
    # One version with comma split, one version without
    df_comma_split, df_no_comma_split = pd.DataFrame(columns=df_columns), pd.DataFrame(columns=df_columns)
    for html in htmls:
        print("Processing " + html[1] + "...")
        new_df = chunk(html[0], html[1])
        print(new_df.head())
        df_comma_split = pd.concat([df_comma_split, new_df])
        df_comma_split.to_csv('chunk_df_comma_split.csv', index=True)
        df_no_comma_split = pd.concat([df_no_comma_split, chunk(html[0], html[1], False)])
        df_no_comma_split.to_csv('chunk_df_no_comma_split.csv', index=True)
        print("Finished processing " + html[1] + ".")
        

if __name__ == '__main__':
    main()