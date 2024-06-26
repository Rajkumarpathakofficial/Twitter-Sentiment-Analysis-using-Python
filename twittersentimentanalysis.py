# Installing kaggle library
!pip install kaggle

#Configuring path to json file
! mkdir ~/.kaggle
! cp kaggle.json ~/.kaggle/
! chmod 600 ~/.kaggle/kaggle.json

#Fetching API dataset from kaggle
!kaggle datasets download -d kazanova/sentiment140

#extracting the file from compressed dataset
from zipfile import ZipFile
dataset = '/content/sentiment140.zip'

with ZipFile(dataset,'r') as zip: # opening in reading mode
  zip.extractall()
  print("dataset extracted successfully")

"""Adding some Dependencies

"""

import numpy as np
import pandas as pd
import re  # regurlar expression
from nltk.corpus import stopwords #natural language toolkit (nltk)
from nltk.stem.porter import PorterStemmer #reduce the words to its root words
from sklearn.feature_extraction.text import TfidfVectorizer # converting textual data into visual
from sklearn.model_selection import train_test_split #spliting data into train and split data
from sklearn.linear_model import LogisticRegression #training with the data
from sklearn.metrics import accuracy_score #calcuate performance and accuracy of our machine leaning model

import nltk
nltk.download('stopwords')

#printing the stopwords in english
print(stopwords.words('english'))

"""just checking in german"""

print(stopwords.words('german'))

twitter_data = pd.read_csv('/content/training.1600000.processed.noemoticon.csv',encoding = 'iSO-8859-1')

twitter_data.shape

twitter_data.head()

"""here colums are not printed so adding the column names"""

column_names= ['target', 'id', 'date', 'flag','user', 'text']
twitter_data = pd.read_csv('/content/training.1600000.processed.noemoticon.csv',names= column_names,encoding = 'iSO-8859-1')

twitter_data.shape

twitter_data.head()

#checking whether there are null values or not
twitter_data.isnull().sum()

"""Checking the distribution of target column here 0 means **negative** 2 means neutral and 4 means **positive**"""

twitter_data['target'].value_counts()

"""Here from the output it seems amoung 1.6 million i,e  16 lakhs tweets 8 lakhs are negative and remaining noes are positive it is distributed in **half**

here 4 and 0 seems odd so lets make **0** and **1** 0 for **negative** and 1 for *positive*
"""

#converting 4 into 1
twitter_data.replace({'target': {4:1}}, inplace =True)

twitter_data['target'].value_counts()

"""**Stemming**

it is the proecss of reducing words

example *nepali*, *nepalese*, *gorkhali*, =**Nepal**

*actor*, *actress*, *acting* = **act**
"""

port_strem = PorterStemmer()

def stemming(content):

  stemmed_content = re.sub('[^a-zA-Z]','',content)
  stemmed_content = stemmed_content.lower()
  stemmed_content = stemmed_content.split()
  stemmed_content =[port_strem.stem(word)for word in stemmed_content if not word in stopwords.words('english')]
  stemmed_content = ' '.join(stemmed_content)

  return stemmed_content

twitter_data['stemmed_content'] = twitter_data['text'].apply(stemming) # it took almost  4 minutes because its testing 1.6 million tweets

twitter_data.tail(10)

print(twitter_data['stemmed_content'])

print(twitter_data['target'])

X = twitter_data['stemmed_content'].values
Y= twitter_data['target'].values

print(X)

print(Y)

X_train, X_test, Y_train, Y_test = train_test_split(X,Y,test_size=0.2, stratify=Y, random_state=2) # 0.2 = 20%

print(X.shape, X_train.shape, X_test.shape)

print(X_train, X_test)

"""Now converting textual data into numerical data target is already 0 and 1 now we will do it to stemmed_content"""

vectorizer = TfidfVectorizer()
X_train = vectorizer.fit_transform(X_train)
X_test = vectorizer.transform(X_test)

print(X_train)

print(X_test)

model = LogisticRegression(max_iter =1000)

model.fit(X_train, Y_train)

X_train_prediction = model.predict(X_train)
training_data_accuracy = accuracy_score(Y_train, X_train_prediction)

print("accuracy score on training data is :", training_data_accuracy)

"""it shows 0.99 that means the accuracy is 99 %"""

X_test_prediction = model.predict(X_test)
test_data_accuracy = accuracy_score(Y_test, X_test_prediction)

print("accuracy score on test data is :", test_data_accuracy)

"""on test data its on 0.51 which is preety low its only 51 %

Model accuracy is 51 %
"""

import pickle

"""Saving the data using pickle library"""

filename = 'trained_model.sav'
pickle.dump(model, open(filename, 'wb'))

"""loading the saved data using future predictions

"""

loaded_model = pickle.load(open('/content/trained_model.sav', 'rb'))

X_new = X_test[200]
print(Y_test[200])
prediction = model.predict (X_new)
print(prediction)

if (prediction[0] == 0):
  print("negative tweet")
else:
  print("positive tweet")

