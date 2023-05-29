# -*- coding: utf-8 -*-
"""webapp.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1SZ254vOXE1nNMZAtRVHKY-9YV2Fg2Wjy
"""

# !pip install streamlit

import streamlit as st
import pickle
import nltk
import numpy as np
import pandas as pd
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer



# Terms must have DF >= 5 to be considered
def tokenizer(text):
    """
    Tokenizes the document
    """
    return word_tokenize(text)



nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
#Load up our stop words
stop_words = stopwords.words('english')
#Adds stuff to our stop words list
stop_words.extend(['.',','])


## This function can improve, simplify. Look into Text Data Lecture
def remove_stopwords(list_of_tokens):
    """
    Removes stopwords
    """
    
    cleaned_tokens = [] 
    
    for token in list_of_tokens: 
        if token in stop_words: continue 
        cleaned_tokens.append(token)
            
    return cleaned_tokens


def stemmer(list_of_tokens):
    '''
    Takes in an input which is a list of tokens, and spits out a list of stemmed tokens.
    '''
    
    stemmed_tokens_list = []
    
    for i in list_of_tokens:
        
        token = PorterStemmer().stem(i)
        stemmed_tokens_list.append(token)
        
    return stemmed_tokens_list

def lemmatizer(list_of_tokens):
    
    lemmatized_tokens_list = []
    
    for i in list_of_tokens: 
        token = WordNetLemmatizer().lemmatize(i)
        lemmatized_tokens_list.append(token)
        
    return lemmatized_tokens_list


def the_untokenizer(token_list):
        '''
        Returns all the tokenized words in the list to one string. 
        Used after the pre processing, such as removing stopwords, and lemmatizing. 
        '''
        return " ".join(token_list)

def cleaning_our_texts(text):
  
  tokenized_list = tokenizer(text)
  removed_stopwords = remove_stopwords(tokenized_list)
  stemmed_words = stemmer(removed_stopwords)
  lemmatized_words = lemmatizer(stemmed_words)
  back_to_string = the_untokenizer(lemmatized_words)
  return back_to_string

genre_cols=['Action', 'Adventure', 'Animation', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family', 'Fantasy', 'Foreign', 'History', 'Horror', 'Music', 'Mystery', 'Romance', 'ScienceFiction', 'TVMovie', 'Thriller', 'War', 'Western']
feature_cols=['id']

from sklearn.preprocessing import StandardScaler 
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib



def predict_genre(text):  
  logreg = pickle.load(open('predictwithLogReg.sav','rb'))
  my_scaler = joblib.load('my_best_scaler.pkl')
  my_tfidf = joblib.load('my_best_tfidf.pkl')
  
  feature_cols_df = pd.DataFrame([[0]*1 ], columns=feature_cols)

 
  
  input_tfidf = my_tfidf.transform([cleaning_our_texts(text)])
  input_transformed_df = pd.DataFrame(input_tfidf.toarray(), columns=my_tfidf.get_feature_names_out())
  input_final = pd.concat([feature_cols_df, input_transformed_df], axis=1)
  
  
 
  X = my_scaler.transform(input_final)
  
  
  prediction = logreg.predict_proba(X)
  
  df = pd.DataFrame(prediction, columns=genre_cols).T.sort_values(0, ascending=False)
  output_list = []
  for index, row in df.iterrows():
    if row.values[0] >= 0.2:
      temp_list = [int(round(row.values[0]*100,0)), index.capitalize()]
      output_list.append(temp_list)

  st.write(output_list)
  return output_list



if __name__ == '__main__':
  st.title("Movie Genre classification")
  models = ['Linear regression', 'SVM']
  text = st.text_area("Write an overview of the movie to predict genre.","John Carter is a war-weary, former military captain who's inexplicably transported to the mysterious and exotic planet of Barsoom (Mars) and reluctantly becomes embroiled in an epic conflict. It's a world on the brink of collapse, and Carter rediscovers his humanity when he realizes the survival of Barsoom and its people rests in his hands.")

 
  chosenModel = st.radio('Select a model to predict', models)
 
  if st.button('Predict'):
      genre_list = predict_genre(text)
      st.success(genre_list)