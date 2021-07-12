import pickle

from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from tensorflow.keras.preprocessing.sequence import pad_sequences
import nltk
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
from tensorflow import keras
nltk.download('stopwords')
import numpy as np

theme_models = [keras.models.load_model('baby_models/model_animals.h5'),
                keras.models.load_model('baby_models/model_body.h5'),
                keras.models.load_model('baby_models/model_family.h5'),
                keras.models.load_model('baby_models/model_love.h5'),
                keras.models.load_model('baby_models/model_nature.h5')]
theme_labels = ['animals', 'body', 'family', 'love', 'nature']


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

def themes_prediction(text, tokenizer):
  global theme_models, theme_labels
  input = preprocess_input(text,tokenizer)
  scores = []
  for model in theme_models:
    res = model.predict(input)
    if res[0][0] >= 0.3:
      scores.append(1)
    else:
      scores.append(0)

  result = []
  for i in range(len(scores)):
    if scores[i] == 1:
      result.append(theme_labels[i])

  if len(result) == 0:
    result.append('living')

  return result

t = """So now I have confessed that he is thine,
And I my self am mortgaged to thy will,
Myself I’ll forfeit, so that other mine
Thou wilt restore to be my comfort still:
But thou wilt not, nor he will not be free,
For thou art covetous, and he is kind;
He learned but surety-like to write for me,
Under that bond that him as fast doth bind.
The statute of thy beauty thou wilt take,
Thou usurer, that put’st forth all to use,
And sue a friend came debtor for my sake;
So him I lose through my unkind abuse.
    Him have I lost; thou hast both him and me:
    He pays the whole, and yet am I not free.
"""

with open('tokenizer1.pickle', 'rb') as handle:
  tokenizer = pickle.load(handle)

model1 = keras.models.load_model('year_prediction.h5')

print(model1.predict(preprocess_input(t,tokenizer)))