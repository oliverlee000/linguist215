import os, re, pandas as pd
'''
parse_df.pycondfa
April 7, 2025

Variety of ways to parse a df to look for metric patterns

Right now, the Strong Metricality methodology found in Borgeson et al. (2020)
is implemented, this time for the fairy tales

NOTE: Assumes installation of espeak - otherwise, program will crash in the prosodify() function
'''

import prosodic

CHUNK_SIZE = 5 # Size of chunks in Borgeon et al. (2020)

'''
Take DataFrame and convert it into Prosodic object Stanza

If filter_rows=True, filters df to rows with exactly 5 words (specified in CHUNK_SIZE final variable)

Returns Stanza
'''
def prosodify(df, filter_rows):
    df = df[df['word_count'] == CHUNK_SIZE] if filter_rows else df
    df_as_string = '\n'.join(df['chunk'].astype(str))
    # df_as_string = "This is a test string\nThis is a test string"
    df_as_stanza = prosodic.Text(df_as_string)
    return df_as_stanza

''''
Applies the Strong Metricality methodology found in Borgeson et al. (2020),
(Sections 2.1-2, pp. 9-13), EXACTLY

- Feeds each line into Prosodic, with five constraints (function names for constraints in parentheses):
   1. *W/PEAK ('w_peak')
   2. *S/UNSTRESSED ('s_unstress')
   3. *W/STRESSED ('w_stress')
   4. WRESOLUTION ('unres_within')
   5. FRESOLUTION ('unres_across') 

Params:
data = fairy tale df as Pandas DataFrame
filter_rows = whether to filter df to rows with exactly CHUNK-SIZE words

Returns:
parsed_df - the df as a Stanza object, parsed for all psosible metrics
df_scores - number of violations for the best parse of each line
df_parses - number of best parses for each line
'''
def strong_metricality(data, constraints, filter_rows=False):
    df_as_stanza = prosodify(data, filter_rows) # Convert into Stanza
    parsed_df = df_as_stanza.parse(constraints=constraints)
    df_scores = parsed_df.df.groupby('line_num', as_index=False)['parse_score'].min()
    df_parses = [len(i.best_parses) for i in parsed_df]
    return parsed_df.df, df_scores, df_parses

'''
Iterate through each html files in data, feed
into strong_metricality().
'''
def main():
    filename = 'chunk_df_comma_split.csv'
    df = pd.read_csv(filename)
    constraints = ('w_peak', 's_unstress', 'w_stress', 'unres_within', 'unres_across')
    parsed_stanza, df_scores, num_parses = strong_metricality(df, constraints=constraints)
    new_fn = os.path.splitext(os.path.basename(filename))[0] + 'prosodified.csv'
    parsed_stanza.to_csv(new_fn)
    mean_violations = df_scores['parse_score'].mean()
    mean_parses = sum(num_parses)/len(num_parses)
    print("Finished.")
    print("Mean number of violations per line:" + str(mean_violations))
    print("Mean number of best parses per line:" + str(mean_parses))
        

if __name__ == '__main__':
    main()