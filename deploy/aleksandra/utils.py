from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from tensorflow.keras.preprocessing.sequence import pad_sequences
import nltk
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
nltk.download('stopwords')
import numpy as np



def full_form(word):
  if word == "nt": word = 'not'
  if word == "re": word = 'be'
  if word == "d": word = 'would'
  if word == "m": word = 'am'
  if word == "s": word = 'be'
  if word == "ve": word = 'have'
  return word


def preprocessing(text):
  tokenizer = RegexpTokenizer(r'\w+')
  text = tokenizer.tokenize(text)
  stop_words = set(stopwords.words('english'))
  cleaned_text = []
  for word in text:
    if word not in stop_words:
      cleaned_text.append(word)
  wnl = WordNetLemmatizer()
  text = [wnl.lemmatize(token) for token in cleaned_text]
  text = [full_form(w).lower() for w in text]
  return text


def preprocess_input(text, tokenizer):
  text = preprocessing(text)
  text = tokenizer.texts_to_sequences(text)
  text2 = []
  for x in text:
    if len(x) != 0:
      text2.append(x[0])
    else:
      text2.append(0)
  maxlen = 150
  text = pad_sequences([text2], padding='post', truncating='post', maxlen=maxlen)
  return np.array([text[0]])

def convert_to_decade(x):
  dec = x // 10
  res = dec * 10
  return res

