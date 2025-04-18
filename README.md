# LINGUIST 215 Corpus Phonology Project

Spring 2025

This project parses a variety of fairy tales in Project Gutenberg to identify rhythmic patterns associated with the genre.

Fairy tales include: 
* Andrew Lang's _The Fairy Tale Books_ (Blue, Blown, Crimson, Orange, Red, Yellow, and Violet editions)
* Jacob and Wilhelm Grimm's _Grimms Fairy Tales_ (Taylor and Edwardes translation)
* Hans Christian Anderssen's _Fairy Tales_

Repository contains:
* data - Folder containing htmls of each fairy tale extracted from Gutenberg
* chunk_df_comma_split.csv - all strings of words from fairy rtales, split by any punctuation mark including commas
* chunk_df_no_comma_split.csv - all strings of words from fairy tales, split by any punctuation mark __except__ commas
* main.py - python script generating chunk_df_comma_split.csv and chunk_df_no_comma_split.csv
