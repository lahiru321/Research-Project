import numpy as np
import pandas as pd
import re
import string
import pickle
import os
from nltk.stem import PorterStemmer
ps = PorterStemmer()


# load model
import os
model_path = os.path.join(os.getcwd(), 'app', 'static', 'model', 'model.pickle')
with open(model_path, 'rb') as f:
    model = pickle.load(f)


# load stopwords
stopwords_path = os.path.join(os.getcwd(), 'app','static', 'model', 'corpora', 'stopwords', 'english')
with open(stopwords_path, 'r') as file:
    sw = file.read().splitlines()

# load tokens
vocab_path = os.path.join(os.getcwd(), 'app','static', 'model', 'vocabulary.txt')
vocab = pd.read_csv(vocab_path, header=None)
tokens = vocab[0].tolist()


def remove_punctuations(text):
    for punctuation in string.punctuation:
        text = text.replace(punctuation, '')
    return text

def preprocessing(text):
    data = pd.DataFrame([text], columns=['tweet'])
    data["tweet"] = data["tweet"].apply(lambda x: " ".join(x.lower() for x in x.split()))
    data["tweet"] = data['tweet'].apply(lambda x: " ".join(re.sub(r'^https?:\/\/.*[\r\n]*', '', x, flags=re.MULTILINE) for x in x.split()))
    data["tweet"] = data["tweet"].apply(remove_punctuations)
    data["tweet"] = data['tweet'].str.replace('\d+', '', regex=True)
    data["tweet"] = data["tweet"].apply(lambda x: " ".join(x for x in x.split() if x not in sw))
    data["tweet"] = data["tweet"].apply(lambda x: " ".join(ps.stem(x) for x in x.split()))
    return data["tweet"]

def vectorizer(ds):
    vectorized_lst = []
    for sentence in ds:
        sentence_lst = np.zeros(len(tokens))
        for i in range(len(tokens)):
            if tokens[i] in sentence.split():
                sentence_lst[i] = 1  
        vectorized_lst.append(sentence_lst)
    vectorized_lst_new = np.asarray(vectorized_lst, dtype=np.float32)
    return vectorized_lst_new

def get_prediction(vectorized_text):
    prediction = model.predict(vectorized_text)
    if prediction == 1:
        return 'negative'
    else:
        return 'positive'