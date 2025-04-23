import os, re, argparse, pandas as pd
'''
parse_df.py
April 7, 2025

Variety of ways to parse a df to look for metric patterns

Right now, the Strong Metricality methodology found in Borgeson et al. (2020)
is implemented, this time for the fairy tales

NOTE: Assumes installation of espeak - otherwise, program will crash in the prosodify() function
'''

import prosodic

'''
Take DataFrame and convert it into Prosodic object Stanza

If args.filter_rows=True, filters df to rows with exactly 5 words (specified in args.chunk_size)

Returns Stanza
'''
def prosodify(df):
    print("Converting into Prosodic object...")
    df_as_string = '\n'.join(df['chunk'].astype(str))
    df_as_stanza = prosodic.Text(df_as_string)
    print("Finished converting into Prosodic object.")
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

Returns:
parsed_df - the df as a Stanza object, parsed for all possible metrics
df_scores - number of violations for the best parse of each line
df_parses - number of best parses for each line
'''
def strong_metricality(data, constraints, args):
    if args.filter_rows:
        data = data[data['word_count'] == args.chunk_size] # if Filter for rows with n(words) = chunk_size 
    
    df_as_stanza = prosodify(data) # Convert into Stanza

    print("Finding all possible meters...")
    parsed_df = df_as_stanza.parse(constraints=constraints) # Run parse

    # Convert into pandas df for easier processing
    df_scores = parsed_df.df.groupby('line_num', as_index=False)['parse_score'].min() # Number of violations for line's best parse
    df_parses = [len(i.best_parses) for i in parsed_df] # Number of parses for a line
    return parsed_df.df, df_scores, df_parses

'''
Iterate through each html files in data, feed
into strong_metricality().
'''
def main(args):
    # Read dataset, set constraints
    filename = 'chunk_df_comma_split_cleaned.csv'
    df = pd.read_csv(filename)
    constraints = ('w_peak', 's_unstress', 'w_stress', 'unres_within', 'unres_across')

    # Run Prosodic
    parsed_stanza, df_scores, num_parses = strong_metricality(df, constraints, args)

    # Save Prosodic output into dataset
    new_fn = os.path.splitext(os.path.basename(filename))[0] + 'prosodified.csv'
    parsed_stanza.to_csv(new_fn)

    # Return statas
    mean_violations = df_scores['parse_score'].mean()
    mean_parses = sum(num_parses)/len(num_parses)
    print("Mean number of violations per line:" + str(mean_violations))
    print("Mean number of best parses per line:" + str(mean_parses))
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                    prog='parse_df.py',
                    description='Variety of ways to parse a df to look for metric patterns')
    parser.add_argument('--filter_rows', action='store_true',help="Whether to filter rows of a given chunk size")
    parser.add_argument('--chunk_size', type=int, default=0,help="Number of words to appear in each line")
    args = parser.parse_args()
    args.filter_rows = (args.chunk_size != 0 or args.filter_rows) # Filter rows if chunk_size arg is specified
    print("Starting parsing with filter_rows = {args.filter_rows}")
    if args.filter_rows:
        print("Filtering for rows with n(words) =  {args.chunk_size}")
    main(args)
    print("Done.")