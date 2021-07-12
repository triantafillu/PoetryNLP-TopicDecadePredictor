import pandas as pd

import json
import string
import spacy

from tensorflow import keras
from keras_preprocessing.text import tokenizer_from_json



def full_form(word):
    if word == 'nt': word = 'not'
    if word == 're': word = 'are'
    if word == 's': word = 'is'
    if word == 'd': word = 'would'
    if word == 'll': word = 'will'
    if word == 't': word = 'not'
    if word == 've': word = 'have'
    if word == 'm': word = 'am'
    return word

def to_lower_case(df_input):
    #  change the texts to lowercase
    df_input['text'] = df_input['text'].str.lower()
    df_input['title'] = df_input['title'].str.lower()
    
    return df_input
    
def rem_punctuation(df_input):
    #  Remove punctuation
    table = str.maketrans('', '', string.punctuation)
    df_input['text'] = [row['text'].translate(table) for index, row in df_input.iterrows()]
    df_input['title'] = [row['title'].translate(table) for index, row in df_input.iterrows()]
    
    return df_input

def lemmatize(df_input):
    #  Lemmatization
    nlp = spacy.load("en_core_web_sm")

    df_input['text'] = [
                    [token.lemma_ for token in nlp(row['text'])]
                    for index, row in df_input.iterrows()
                 ]
    df_input['title'] = [
                    [token.lemma_ for token in nlp(row['title'])]
                    for index, row in df_input.iterrows()
                 ]
    
    return df_input
    

def tokenize(df_input):
    #Load tokenizator
    import os
    print(os.path.abspath(os.getcwd()))
    with open('flask-app/tokenizer.json') as f: 
        data_tok = json.load(f) 
        tok = tokenizer_from_json(data_tok)
    
    df_input['text'] = tok.texts_to_sequences(df_input['text'])
    df_input['title'] = tok.texts_to_sequences(df_input['title'])
    
    return df_input
    

def preprocess_input(df_input):
    #  set up data types
    df_input = df_input.astype({'text': 'str'})

    df_input = to_lower_case(df_input)

    df_input = rem_punctuation(df_input)
    
    #  Remove stopwords
    from spacy.lang.en.stop_words import STOP_WORDS
    df_input['text'] = df_input['text'].apply(lambda x: " ".join(x for x in x.split() if x not in STOP_WORDS))
    
    df_input = lemmatize(df_input)
    
    df_input['text'] = [
                [full_form(w) for w in row['text']]
                for index, row in df_input.iterrows()
             ]
    
    df_input = tokenize(df_input)
        
        
    max_len = 150  # max length of string
    joined_text = df_input['title'] + df_input['text']
    X = keras.preprocessing.sequence.pad_sequences(list(joined_text), maxlen=max_len, padding='post')
    
    return X
